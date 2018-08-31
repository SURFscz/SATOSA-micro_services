"""
A concept breakout example module for the satosa proxy
Be carefull! InternalResponse.name_id is lost after serialization
This means that any micro_service making use of InternalResponse.name_id
like custom_uid MUST precede this one
"""
import logging
import pickle

from ..internal_data import InternalResponse
from ..logging_util import satosa_logging
from ..micro_services.base import ResponseMicroService
from ..response import Redirect

logger = logging.getLogger(__name__)
STATE_KEY = "BREAKOUT"

class BreakOut(ResponseMicroService):
    """
    Example module to show how to break out of satosa flow and return
    """

    def __init__(self, config, internal_attributes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "breakout"
        self.endpoint = "/resume"
        self.redirect_url = config["redirect_url"]
        self.resumed = False
        logger.info("Breakout micro_service is active")

    def register_endpoints(self):
        """
        Register breakout module endpoints
        :return: A list of endpoints bound to a function
        """
        logger.info("Register BreakOut endpoint")
        return [("^breakout%s$" % self.endpoint, self._handle_endpoint)]

    def process(self, context, internal_response):
        logger.info("Process BreakOut")
        context.state[STATE_KEY] = {}
        context.state[STATE_KEY]["internal_resp"] = internal_response.to_dict()
        logger.info("internal_resp: %s" % context.state[STATE_KEY]["internal_resp"])
        return self._check_requirement(context, internal_response)

    def _check_requirement(self, context, internal_response):
        logger.info("Check BreakOut requirement")
        if self.resumed:
            return super().process(context, internal_response)
        else:
            return Redirect(self.redirect_url)

    def _handle_endpoint(self, context):
        logger.info("Handle BreakOut endpoint")

        breakout_state = context.state[STATE_KEY]
        saved_response = breakout_state["internal_resp"]
        logger.info("internal_resp: %s" % saved_response)
        internal_response = InternalResponse.from_dict(saved_response)
        self.resumed = True
        return self._check_requirement(context, internal_response)
