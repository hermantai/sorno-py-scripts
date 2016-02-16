"""Tests for sorno.webutil


Copyright 2015 Heung Ming Tai

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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest

from sorno import webutil


class HtmlTestCase(unittest.TestCase):
    def test_unquote_url_EmptyString(self):
        self.assertEqual('', webutil.unquote_url(''))

    def test_unquote_url_NoSpecialCharacter_ReturnAsIs(self):
        self.assertEqual(
            'http://abc.com',
            webutil.unquote_url('http://abc.com'),
        )

    def test_unquote_url_OneEncodedCharacter_ReturnUnquoted(self):
        self.assertEqual(
            'http://abc.com/hello world',
            webutil.unquote_url('http://abc.com/hello%20world'),
        )


if __name__ == '__main__':
    unittest.main()
