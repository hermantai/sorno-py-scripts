"""
Unit test for sorno_replace_thrift_const

   Copyright 2014 Herman Tai

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from sorno_replace_thrift_const import ThriftConstReplacer

import unittest


class ThriftConstReplacerTestCase(unittest.TestCase):
    def setUp(self):
        self.replacer = ThriftConstReplacer()

    def test_parse_line_SimpleLine_ReturnAsIsNoConstsSet(self):
        line = "// abcdefg"
        output = self.replacer.parse_line(line)
        self.assertEqual(line, output)
        self.assertEqual({}, self.replacer.get_consts())

    def test_parse_line_ConstantDeclaration_ConstsSet(self):
        const = '"abc"'
        line = "const string a = " + const + ";"
        output = self.replacer.parse_line(line)
        self.assertEqual(line, output)
        self.assertEqual({'a': const}, self.replacer.get_consts())

    def test_parse_line_ConstantDeclarationThenUsed_ConstReplaced(self):
        const = '"abc"'
        line = "const string a = " + const
        self.replacer.parse_line(line)

        line2 = "a + xyz"
        output = self.replacer.parse_line(line2)
        self.assertEqual('"abc" + xyz', output)

    def test_parse_line_ConstantDeclarationThenUsedWithCommas_ConstReplaced(
        self
    ):
        const = '"abc"'
        line = "const string a = " + const
        self.replacer.parse_line(line)

        line2 = "a, + xyz"
        output = self.replacer.parse_line(line2)
        self.assertEqual('"abc", + xyz', output)

    def test_parse_line_ValueHasSpace_ConstReplaced(self):
        const = '"abc def"'
        line = "const string a = " + const
        self.replacer.parse_line(line)

        line2 = "a + xyz"
        output = self.replacer.parse_line(line2)
        self.assertEqual('"abc def" + xyz', output)

    def test_parse_line_ValueAtSeparateLine_ConstReplaced(self):
        const = '"abc def"'
        line1 = "const string a ="
        line2 = const
        self.replacer.parse_line(line1)
        self.replacer.parse_line(line2)

        line3 = "a + xyz"
        output = self.replacer.parse_line(line3)
        self.assertEqual('"abc def" + xyz', output)


if __name__ == '__main__':
    unittest.main()
