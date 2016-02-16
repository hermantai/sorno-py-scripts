"""
Tests for sorno_amazon_reviews_scrape


   Copyright 2014 Heung Ming Tai

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

from sorno_amazon_reviews_scrape import App


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = App("blah")

    def test_get_text_from_element_NodeWithTextOnly(self):
        e = html.fromstring("<a>abcd</a>")
        self.assertEquals("abcd", self.app.get_text_from_element(e))

    def test_get_text_from_element_NodeWithTextAndOneChild(self):
        e = html.fromstring("<a>abcd<c1 />efg</a>")
        self.assertEquals("abcdefg", self.app.get_text_from_element(e))

    def test_get_text_from_element_NodeWithTextAndTwoChildren(self):
        e = html.fromstring("<a>abc<c1/>def</c2>ghi</a>")
        self.assertEquals("abcdefghi", self.app.get_text_from_element(e))

    def test_get_text_from_element_NodeWithTextAndNestedText(self):
        e = html.fromstring("<a>abc<c1>def</c1></c2>ghi</a>")
        self.assertEquals("abcdefghi", self.app.get_text_from_element(e))

    def test_get_text_from_element_NodeWithTextAndBRElement(self):
        e = html.fromstring("<a>abc<br />def</a>")
        self.assertEquals(
            "abc" + os.linesep + "def",
            self.app.get_text_from_element(e)
        )

    def test_get_text_from_element_NodeWithTextAndMultiBRElement(self):
        e = html.fromstring("<a>abc<br /><br />def<br />ghi<br /></a>")
        self.assertEquals(
            "abc" + os.linesep + os.linesep + "def" + os.linesep + "ghi"
                + os.linesep,
            self.app.get_text_from_element(e)
        )

    def test_get_main_url_and_page_number_PlainURL_PageNumber1(self):
        url, n = self.app.get_main_url_and_page_number(
            "http://www.abc.com/product-reviews/"
        )
        self.assertEquals(1, n)
        self.assertEquals("http://www.abc.com/product-reviews/", url)

    def test_get_main_url_and_page_number_URLWithNumber2_PageNumber2(self):
        url, n = self.app.get_main_url_and_page_number(
            "http://www.abc.com/product-reviews/?pageNumber=2"
        )
        self.assertEquals(2, n)
        self.assertEquals("http://www.abc.com/product-reviews/", url)

    def test_get_main_url_and_page_number_URLWithNumber2AndOtherParam_PageNumber2(self):
        url, n = self.app.get_main_url_and_page_number(
            "http://www.abc.com/product-reviews/?a=apple&pageNumber=2"
        )
        self.assertEquals(2, n)
        self.assertEquals("http://www.abc.com/product-reviews/", url)


if __name__ == '__main__':
    unittest.main()
