from unittest import TestCase
from uuid import uuid4

from munch import munchify
from satosa.logging_util import LOGGER_STATE_KEY

from src.scz_micro_services.custom_uid import CustomUID


class TestCustomUid(TestCase):

    def test_custom_uid(self):
        context = munchify({"state": {LOGGER_STATE_KEY: uuid4().urn, "IDHASHER": {}},
                            "select": ["eduPersonPrincipalName", "eduPersonTargetedID"],
                            "custom_attribute": "cmuid",
                            "user_id": True})
        c_uid = CustomUID(context, name="custom_uid", base_url="http://localhost")

        def next_call(ctx={}, data={}):
            pass

        c_uid.__dict__["next"] = next_call

        self.assertEqual(c_uid.logprefix, "CUSTOM_UID:")

        data = munchify({"name_id": "urn:john", "attributes": {"eduPersonPrincipalName": "urn:john",
                                                               "eduPersonTargetedID": "urn:target"}})
        c_uid.process(context, data)

        self.assertEqual("u|r|n|:|j|o|h|n|u|r|n|:|t|a|r|g|e|t", data.user_id)
