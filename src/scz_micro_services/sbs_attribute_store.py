# -*- coding: future_fstrings -*-
"""
SATOSA microservice that uses an identifier asserted by
the home organization SAML IdP as a key to query the SBS API
for attributes assert them to the receiving SP.
"""

import copy
import logging

import requests
from satosa.attribute_mapping import AttributeMapper
from satosa.logging_util import satosa_logging
from satosa.micro_services.base import ResponseMicroService

logger = logging.getLogger("satosa")


class SBSAttributeStore(ResponseMicroService):
    log_prefix = "SBS_ATTRIBUTE_STORE:"
    attribute_profile = "saml"

    def __init__(self, config, internal_attributes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.converter = AttributeMapper(internal_attributes)

    @staticmethod
    def _debug(msg, context):
        satosa_logging(logger, logging.DEBUG, msg, context.state)

    def process(self, context, data):
        config_clean = copy.deepcopy(self.config)
        if "sbs_api_password" in config_clean:
            del config_clean["sbs_api_password"]

        self._debug(f"{self.log_prefix} Using default configuration {config_clean}", context)

        # Find the entityID for the SP that initiated the flow and target IdP
        try:
            sp_entity_id = context.state.state_dict["SATOSA_BASE"]["requester"]
            idp_entity_id = data.auth_info.issuer
        except KeyError:
            satosa_logging(logger, logging.ERROR,
                           f"{self.log_prefix} Unable to determine the entityID's for the IdP or SP", context.state)
            return super().process(context, data)

        self._debug(f"{self.log_prefix} entityID for the requester is {sp_entity_id}", context)
        self._debug(f"{self.log_prefix} entityID for the source IdP is {idp_entity_id}", context)

        try:
            sbs_api_user = self.config["sbs_api_user"]
            sbs_api_password = self.config["sbs_api_password"]
            sbs_api_base_url = self.config["sbs_api_base_url"]
            sbs_blacklist = self.config.get("sbs_blacklist") or []

        except KeyError as err:
            satosa_logging(logger, logging.ERROR, f"{self.log_prefix} Configuration {err} is missing", context.state)
            return super().process(context, data)

        if sp_entity_id in sbs_blacklist:
            satosa_logging(logger, logging.DEBUG, f"{self.log_prefix} Skipping lookup for {sp_entity_id}", context.state)
            return super().process(context, data)

        res = requests.get(f"{sbs_api_base_url}api/users/attributes",
                           params={"service_entity_id": sp_entity_id, "uid": data.user_id},
                           auth=(sbs_api_user, sbs_api_password))
        if res.status_code != 200:
            satosa_logging(logger, logging.ERROR, f"{self.log_prefix} Error response {res.status_code} from SBS",
                           context.state)
            return super().process(context, data)

        json_response = res.json()
        self._debug(f"{self.log_prefix} Response from SBS: {json_response}", context)

        internal = self.converter.to_internal(self.attribute_profile, json_response)
        for k, v in internal.items():
            data.attributes[k] = v

        self._debug(f"{self.log_prefix} returning data.attributes {data.attributes}", context)
        return super().process(context, data)
