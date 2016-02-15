"""Tests for sorno.dictutil.py"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from sorno import dictutil


class DefaultDictWithEnhancedFactoryTestCase(unittest.TestCase):
    def test_keyNotMissing_getOriginalValueBack(self):
        d = dictutil.DefaultDictWithEnhancedFactory(None)
        d['a'] = "apple"
        self.assertEqual("apple", d['a'])

    def test_identityDefaultFactory(self):
        d = dictutil.DefaultDictWithEnhancedFactory(lambda k: k)
        self.assertEqual("apple", d['apple'])
