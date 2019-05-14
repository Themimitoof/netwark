import pytest
import unittest

from ..helpers import domain


class TestHelperDomain(unittest.TestCase):
    def test_is_valid_fqdn(self):
        is_valid = domain.is_valid_fqdn('hello.com')
        self.assertTrue(is_valid)

        is_valid = domain.is_valid_fqdn('xn--ls8haaaa.com')
        self.assertTrue(is_valid)

        is_false = domain.is_valid_fqdn('💩💩💩💩💩.com')
        self.assertFalse(is_false)

        is_false = domain.is_valid_fqdn('pile-of-poooooo-.com')
        self.assertFalse(is_false)

    def test_domain_to_idna(self):
        idna = domain.to_idna('héllo.com')
        self.assertEqual(idna, 'xn--hllo-bpa.com')

        idna = domain.to_idna('💩💩💩💩💩.com')
        self.assertEqual(idna, 'xn--ls8haaaa.com')

        idna = domain.to_idna('インターネットはいい.com')
        self.assertEqual(idna, 'xn--n8ja1kti1eya9a0b20a7c.com')
