"""Tests for sorno.consoleutil


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

from mock import patch
import unittest

from sorno import consoleutil
from sorno import mathlib


class ConsoleutilTestCase(unittest.TestCase):
    def test_parse_intervals_EmptyString_EmptyList(self):
        self.assertEqual([], consoleutil.parse_intervals(""))

    def test_parse_intervals_OneNum_OneInterval(self):
        self.assertEqual(
            [mathlib.Interval(1, 1)],
            consoleutil.parse_intervals("1"),
        )

    def test_parse_intervals_OneInterval_OneInterval(self):
        self.assertEqual(
            [mathlib.Interval(1, 2)],
            consoleutil.parse_intervals("1-2"),
        )

    def test_parse_intervals_TwoIntervalsOneNumberEach_TwoIntervals(self):
        self.assertEqual(
            [mathlib.Interval(1, 1), mathlib.Interval(2, 2)],
            consoleutil.parse_intervals("1,2"),
        )

    def test_parse_intervals_TwoIntervalsTwoNumbersEach_TwoIntervals(self):
        self.assertEqual(
            [mathlib.Interval(1, 3), mathlib.Interval(5, 6)],
            consoleutil.parse_intervals("1-3,5-6"),
        )

    @patch("six.moves.input")
    def test_confirm_GivenAllKindsOfYesResponse_ReturnsTrue(self, input_mock):
        input_mock.return_value = "Y"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "y"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "Yes"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "yes"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "T"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "t"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "True"
        self.assertTrue(consoleutil.confirm("Hello?"))
        input_mock.return_value = "true"
        self.assertTrue(consoleutil.confirm("Hello?"))

    @patch("six.moves.input")
    def test_confirm_GivenAllKindsOfNoResponse_ReturnsTrue(self, input_mock):
        input_mock.return_value = "N"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "n"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "No"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "no"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "F"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "f"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "False"
        self.assertFalse(consoleutil.confirm("Hello?"))
        input_mock.return_value = "false"
        self.assertFalse(consoleutil.confirm("Hello?"))

    @patch("six.moves.input")
    def test_confirm_ResponseIllegalThenYes_ReturnsTrue(self, input_mock):
        input_mock.side_effect = ("blah", "y")
        self.assertTrue(consoleutil.confirm("Hello?"))

    @patch("six.moves.input")
    def test_confirm_ResponseIllegalThenNo_ReturnsTrue(self, input_mock):
        input_mock.side_effect = ("blah", "n")
        self.assertFalse(consoleutil.confirm("Hello?"))
