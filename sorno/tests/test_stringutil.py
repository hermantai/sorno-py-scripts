from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from sorno import stringutil


class StringUtilTestCase(unittest.TestCase):
    def test_oneline_empty_empty(self):
        self.assertEqual("", stringutil.oneline(""))

    def test_oneline_strWithNewLine_becomesSpaces(self):
        s = """
        a
        b
        c
        d
        """
        self.assertEqual("a b c d", stringutil.oneline(s))
