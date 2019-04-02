import logging
import unittest

from ..helpers import ip


class TestHelperIp(unittest.TestCase):
    def test_if_is_ip_equal_true(self):
        result = ip.is_ip('192.168.1.1')
        self.assertTrue(result)

        result = ip.is_ip('fe80::beef:b00f')
        self.assertTrue(result)

    def test_if_is_ip_equal_false(self):
        result = ip.is_ip('192.168.1.0/24')
        self.assertFalse(result)

        result = ip.is_ip('192.168.1.256')
        self.assertFalse(result)

        result = ip.is_ip('192.168.1')
        self.assertFalse(result)

        result = ip.is_ip('gno')
        self.assertFalse(result)

        result = ip.is_ip('2004:3213:b00f:404:3d:ddddd:beef')
        self.assertFalse(result)

        result = ip.is_ip('9999::/24')
        self.assertFalse(result)

    def test_ip_type(self):
        pass

    def test_get_ptr(self):
        pass

    def test_get_whois(self):
        pass
