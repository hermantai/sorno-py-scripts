"""Tests for sorno.mathlib


Copyright 2015 Herman Tai

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

from sorno import mathlib


class IntervalTestCase(unittest.TestCase):
    def test_init_ClosedIntervalByDefault(self):
        intv = mathlib.Interval(1,2)
        self.assertFalse(intv.is_start_opened)
        self.assertFalse(intv.is_end_opened)

    def test_init_StartAndEndAsExpected(self):
        intv = mathlib.Interval(1,2)
        self.assertEqual(1, intv.start)
        self.assertEqual(2, intv.end)

    def test_init_SetIsStartOpened(self):
        intv = mathlib.Interval(1,2, is_start_opened=True)
        self.assertTrue(intv.is_start_opened)
        self.assertFalse(intv.is_end_opened)

    def test_init_SetIsEndOpened(self):
        intv = mathlib.Interval(1,2, is_end_opened=True)
        self.assertFalse(intv.is_start_opened)
        self.assertTrue(intv.is_end_opened)

    def test_eq_AllPropertiesTheSame_True(self):
        intv1 = mathlib.Interval(1,2, is_start_opened=True, is_end_opened=True)
        intv2 = mathlib.Interval(1,2, is_start_opened=True, is_end_opened=True)
        self.assertEqual(intv1, intv2)

    def test_eq_startIsDifferent_False(self):
        intv1 = mathlib.Interval(1,2, is_start_opened=True, is_end_opened=True)
        intv2 = mathlib.Interval(0,2, is_start_opened=True, is_end_opened=True)
        self.assertNotEqual(intv1, intv2)

    def test_eq_DifferentObject_False(self):
        intv1 = mathlib.Interval(1,2, is_start_opened=True, is_end_opened=True)
        self.assertNotEqual(intv1, 1)
