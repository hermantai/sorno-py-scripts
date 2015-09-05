"""
Unit test for sorno_pick

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

from lxml import html
import os
import unittest

import sorno_pick


class PickerAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = sorno_pick.PickerApp()

    def test_filter_out_items_NoItems(self):
        self.assertEqual([], self.app.filter_out_items([]))

    def test_filter_out_items_ExcludeRegex_EverythingExceptMatched(self):
        items = ["a", "b", "c"]
        expected = ["b", "c"]
        self.app.exclude_regexes = ["a"]
        self.assertEqual(expected, self.app.filter_out_items(items))

    def test_filter_out_items_2ExcludeRegexex_EverythingExceptMatched(self):
        items = ["a", "b", "c"]
        expected = ["c"]
        self.app.exclude_regexes = ["a", "b"]
        self.assertEqual(expected, self.app.filter_out_items(items))

    def test_filter_out_items_IncludeOneRegex_ReturnMatched(self):
        items = ["a", "b", "c"]
        expected = ["a"]
        self.app.regexes = ["a"]
        self.assertEqual(expected, self.app.filter_out_items(items))

    def test_filter_out_items_IncludeTwoConflictRegexes_EmptyList(self):
        items = ["a", "b", "c"]
        expected = []
        self.app.regexes = ["a", "b"]
        self.assertEqual(expected, self.app.filter_out_items(items))

    def test_filter_out_items_1Include1ExcludeRegex(self):
        items = ["abc", "bcd", "cdt"]
        expected = ["bcd"]
        self.app.regexes = ["b"]
        self.app.exclude_regexes = ["ab"]
        self.assertEqual(expected, self.app.filter_out_items(items))


if __name__ == "__main__":
    unittest.main()
