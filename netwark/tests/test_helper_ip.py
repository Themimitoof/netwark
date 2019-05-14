import pytest
import unittest
from unittest import mock

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
        result = ip.ip_type('1.1.1.1')
        self.assertEqual('global', result['type'])
        self.assertEqual(4, result['version'])
        self.assertTrue(result['public'])

        result = ip.ip_type('2003::4')
        self.assertEqual('global', result['type'])
        self.assertEqual(6, result['version'])
        self.assertTrue(result['public'])

        result = ip.ip_type('10.10.0.0')
        self.assertEqual('private', result['type'])
        self.assertEqual(4, result['version'])
        self.assertFalse(result['public'])

        with pytest.raises(Exception):
            ip.ip_type('gno')

    def test_get_ptr(self):
        with mock.patch(
            'netwark.helpers.ip.get_ptr', return_value="one.one.one.one."
        ):
            result = ip.get_ptr('1.1.1.1')
        self.assertEqual('one.one.one.one.', result)

    def test_get_whois(self):
        whois = []

        with mock.patch(
            'netwark.helpers.ip.get_ptr', return_value="one.one.one.one."
        ):
            result = ip.get_ptr('1.1.1.1')
        self.assertEqual('one.one.one.one.', result)
