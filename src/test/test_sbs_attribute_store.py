import json
import os
from unittest import TestCase

import requests_mock
import yaml
from munch import munchify

from src.scz_micro_services.sbs_attribute_store import SBSAttributeStore


class TestSBSAttributeStore(TestCase):

    @staticmethod
    def _read_file(file_name):
        file = f"{os.path.dirname(os.path.realpath(__file__))}/{file_name}"
        with open(file) as f:
            return f.read()

    @requests_mock.mock()
    def test_process(self, m):
        config = munchify({
            "sbs_api_user": "sysread",
            "sbs_api_password": "secret",
            "sbs_api_base_url": "http://localhost/"})
        data = self._do_test_process(m, config)

        attributes = data.attributes
        self.assertListEqual(["urn:john"], attributes.uid)
        self.assertListEqual(["Postal 1234AA"], attributes.address)
        self.assertListEqual(["john@example.org", "john@org.com"], sorted(attributes.mail))
        self.assertListEqual(["AI computing", "ai_res"], sorted(attributes.isMemberOf))
        self.assertListEqual(["John Doe"], attributes.name)

    @requests_mock.mock()
    def test_process_missing_key(self, m):
        config = munchify({})
        data = self._do_test_process(m, config)
        self.assertEqual(0, len(data.attributes))

    @requests_mock.mock()
    def test_process_404(self, m):
        config = munchify({
            "sbs_api_user": "sysread",
            "sbs_api_password": "secret",
            "sbs_api_base_url": "http://localhost/"})
        data = self._do_test_process(m, config, status_code=404)

        self.assertEqual(0, len(data.attributes))

    @requests_mock.mock()
    def test_process_missing_requester(self, m):
        config = munchify({
            "sbs_api_user": "sysread",
            "sbs_api_password": "secret",
            "sbs_api_base_url": "http://localhost/"})
        data = self._do_test_process(m, config, satosa_base_requester_key="nope")

        self.assertEqual(0, len(data.attributes))

    def _do_test_process(self, m, config, satosa_base_requester_key="requester", status_code=200):
        internal_attributes = yaml.load(self._read_file("internal_attributes.yaml"))
        sbs_attribute_store = SBSAttributeStore(config,
                                                internal_attributes,
                                                name="sbs_attribute_store",
                                                base_url="http://localhost")

        def next_call(ctx={}, data={}):
            pass

        sbs_attribute_store.__dict__["next"] = next_call
        data = munchify({"user_id": "urn:john", "attributes": {}, "auth_info": {"issuer": "https://idp"}})
        context = munchify(
            {"state": {"state_dict": {"SATOSA_BASE": {satosa_base_requester_key: "https://service_id"}}}})
        m.get("http://localhost/api/user_service_profiles/attributes",
              json=json.loads(self._read_file("mock/sbs_attributes.json")),
              status_code=status_code)
        sbs_attribute_store.process(context, data)
        return data
