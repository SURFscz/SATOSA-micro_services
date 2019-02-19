from unittest import TestCase
from uuid import uuid4

from munch import munchify
from satosa.logging_util import LOGGER_STATE_KEY

from src.scz_micro_services.custom_uid import CustomUID


class TestCustomUid(TestCase):

    def test_custom_uid(self):
        context = munchify({"state": {LOGGER_STATE_KEY: uuid4().urn, "IDHASHER": {}},
                            "select": {"a": "b", "c": "d"},
                            "custom_attribute": "",
                            "user_id": "urn:john"})
        c_uid = CustomUID(context, name="custom_uid", base_url="http://localhost")

        def next_call(ctx={}, data={}):
            pass

        c_uid.__dict__["next"] = next_call

        self.assertEqual(c_uid.logprefix, "CUSTOM_UID:")

        data = munchify({"name_id": "urn:john", "attributes": {"a": "b1", "c": "d1"}})
        c_uid.process(context, data)

        self.assertEqual("b|1|d|1", data.user_id)
