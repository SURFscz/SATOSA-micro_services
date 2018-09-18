"""
Micro Service that extracts info from IdP metadata if available
"""
import logging

from ..internal_data import InternalResponse
from ..logging_util import satosa_logging
from ..micro_services.base import ResponseMicroService

logger = logging.getLogger(__name__)

class MetaInfo(ResponseMicroService):
    """
    Metadata info extracting micro_service
    """

    def __init__(self, config, internal_attributes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.displayname = config.get('displayname', 'idp_name')
        self.country = config.get('country', 'idp_country')
        logger.info("MetaInfo micro_service is active %s, %s " % (self.displayname, self.country))

    def _get_registration_authority(self, md):
        extensions = md.get('extensions')
        if extensions:
            for ee in extensions.get('extension_elements'):
                if 'registration_authority' in ee:
                    return ee['registration_authority']
        return None

    def _get_ra_country(self, ra):
        if ra == "https://incommon.org":
            return "us"
        if ra == "http://kafe.kreonet.net":
            return "kr"
        if ra == "http://www.csc.fi/haka":
            return "fi"
        if ra:
            return ra.split(".")[-1].replace("/","")
        else:
            return None

    def process(self, context, internal_response):
        name = "unknown"
        ra = None
        country = "unknown"

        logger.info("Process MetaInfo")
        issuer = internal_response.auth_info.issuer
        logger.info("Issuer: %s" % issuer)
        metadata_store = context.internal_data.get('metadata_store')
        if metadata_store:
            name = metadata_store.name(issuer)
            ra = self._get_registration_authority(metadata_store[issuer])
            country = self._get_ra_country(ra)

        internal_response.attributes[self.displayname] = [name]
        internal_response.attributes[self.country] = [country]

        logger.info("Name: %s" % name)
        logger.info("RegAuth: %s" % ra)
        logger.info("Country: %s" % country)

        return super().process(context, internal_response)
