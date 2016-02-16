"""Tests for sorno_attach_realdate"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import unittest

import sorno_attach_realdate


class AttachRealDateAppTestCase(unittest.TestCase):
    def setUp(self):
        self.args = lambda: None
        self.args.datetime_format = sorno_attach_realdate._datetime_format
        self.app = sorno_attach_realdate.AttachRealDateApp(self.args)

    def test_aggressive_process_lineWithNoDatetimeString_getItBack(self):
        line = "abc"
        self.assertEqual(
            line,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithDatetimeString(self):
        line = "hello 2006-01-02T15:04:05-0700 world"
        expected = "hello 2006-01-02T15:04:05-0700(2006-01-02 14:04:05) world"

        self.assertEqual(
            expected,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithShortDateString_originalLine(self):
        line = "hello 2006-11-02 world"

        self.assertEqual(
            line,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithDatetimeInQuotes(self):
        line = "hello '2006-01-02T15:04:05-0700' world"
        expected = "hello '2006-01-02T15:04:05-0700'(2006-01-02 14:04:05) world"

        self.assertEqual(
            expected,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithDatetimeInSpecialChars(self):
        line = "hello {'2006-01-02T15:04:05-0700'} world"
        expected = (
            "hello {'2006-01-02T15:04:05-0700'}(2006-01-02 14:04:05) world"
        )

        self.assertEqual(
            expected,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithDatetimeAndCharsInSpecialChars(self):
        line = "hello {'2006-01-02T15:04:05Z'} world"
        expected = (
            "hello {'2006-01-02T15:04:05Z'}(2006-01-02 07:04:05) world"
        )

        self.assertEqual(
            expected,
            self.app._aggressive_process(line),
        )

    def test_aggressive_process_lineWithDtWithNewlineAtTheEnd(self):
        line = "hello 2006-01-02T15:04:05-0700\n"
        expected = "hello 2006-01-02T15:04:05-0700(2006-01-02 14:04:05)\n"

        self.assertEqual(
            expected,
            self.app._aggressive_process(line),
        )

