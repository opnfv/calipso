from discover.cli_fetch_instance_vnics_vpp import CliFetchInstanceVnicsVpp
from test.fetch.cli_fetch.test_data.cli_fetch_instance_vnics import *
from test.fetch.test_fetch import TestFetch


class TestCliFetchInstanceVnicsVpp(TestFetch):

    def setUp(self):
        self.configure_environment()
        self.fetcher = CliFetchInstanceVnicsVpp()

    def test_get_name(self):
        name = self.fetcher.get_vnic_name(VNIC, INSATNCE)
        self.assertNotEqual(name, None, "Can't get vnic name")