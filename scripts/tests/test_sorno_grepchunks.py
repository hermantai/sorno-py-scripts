"""
Tests for sorno_grepchunks


   Copyright 2016 Herman Tai

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

from mock import MagicMock
import re
import unittest

from sorno_grepchunks import GrepChunksApp


class AppTest(unittest.TestCase):
    def setUp(self):
        self.args = MagicMock
        self.args.regex = "test_regex"
        self.app = GrepChunksApp(self.args)

    def test_feed_ThreeLinesNotMatch_OneChunk(self):
        text = "apple\norange\nboy"
        regex = re.compile("zzz")
        for line in text.split('\n'):
            self.assertIsNone(self.app._feed(line, regex))

        self.assertEqual(
            text.replace('\n', ''),
            self.app._close_partial_chunk(),
        )

    def test_feed_ThreeLinesOneLineMatch_TwoChunks(self):
        t1 = "apple"
        t2 = "orange"
        t3 = "boy"

        regex = re.compile("orange")

        self.assertIsNone(self.app._feed(t1, regex))
        self.assertEqual("apple", self.app._feed(t2, regex))
        self.assertIsNone(self.app._feed(t3, regex))

        self.assertEqual("orangeboy", self.app._close_partial_chunk())

    def test_grep_if_exists_RegexMatch(self):
        t1 = "apple"

        self.args.regex = "pp"
        app = GrepChunksApp(self.args)

        self.assertEqual(t1, app._grep_if_exists(t1))

    def test_grep_if_exists_RegexNotMatch(self):
        t1 = "apple"

        self.args.regex = "aa"
        app = GrepChunksApp(self.args)

        self.assertIsNone(app._grep_if_exists(t1))

    def test_grep_if_exists_MultiLineRegexMatch(self):
        t1 = "ap\nple"

        self.args.regex = "p.p"
        app = GrepChunksApp(self.args)

        self.assertEqual(t1, app._grep_if_exists(t1))
