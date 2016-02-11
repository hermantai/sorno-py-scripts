"""Tests for sorno.datetimeutil


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

import datetime
import re
import unittest

from sorno import datetimeutil
import pytz

class DatetimeutilTestCase(unittest.TestCase):
    def setUp(self):
        self.los_angeles_time_zone = pytz.timezone("America/Los_Angeles")
        self.pst_to_pdt_date = datetime.datetime(2016, 3, 13)
        self.pstTimeOnPstToPdtDate = self.pst_to_pdt_date.replace(hour=1)
        self.pdtTimeOnPstToPdtDate = self.pst_to_pdt_date.replace(hour=3)

    def test_datetime_to_timestamp_pstWorksFine(self):
        tz = self.los_angeles_time_zone
        one_am = self.pst_to_pdt_date.replace(hour=1)
        d = tz.normalize(tz.localize(one_am))

        self.assertEqual(
                1457859600,
                datetimeutil.datetime_to_timestamp(d),
        )

    def test_datetime_to_timestamp_pdtWorksFine(self):
        tz = self.los_angeles_time_zone
        three_am = self.pst_to_pdt_date.replace(hour=3)
        d = tz.normalize(tz.localize(three_am))

        self.assertEqual(
            1457863200,
            datetimeutil.datetime_to_timestamp(d),
        )

    def test_timestamp_to_local_datetime_pstWorksFine(self):
        self.assertEqual(
            "2016-03-13T01:00:00-0800PST",
            datetimeutil.timestamp_to_local_datetime(1457859600).strftime(
                datetimeutil.ISO_FORMAT_WITH_TZ_NAME
            ),
        )

    def test_timestamp_to_local_datetime_pdtWorksFine(self):
        self.assertEqual(
            "2016-03-13T03:00:00-0700PDT",
            datetimeutil.timestamp_to_local_datetime(1457863200).strftime(
                datetimeutil.ISO_FORMAT_WITH_TZ_NAME
            ),
        )

    def test_number_to_local_datetime_InSecs(self):
        d = datetimeutil.real_localize(
            datetime.datetime(2016, 3, 12),
            datetimeutil.LOCAL_TIMEZONE,
        )
        ts = datetimeutil.datetime_to_timestamp(d)

        guessed_dt, unit = datetimeutil.number_to_local_datetime(ts)
        self.assertEqual(d, guessed_dt)
        self.assertEqual("s", unit)

    def test_number_to_local_datetime_InMillis(self):
        d = datetimeutil.real_localize(
            datetime.datetime(2016, 3, 12),
            datetimeutil.LOCAL_TIMEZONE,
        )
        ts = datetimeutil.datetime_to_timestamp(d) * 1000

        guessed_dt, unit = datetimeutil.number_to_local_datetime(ts)
        self.assertEqual(d, guessed_dt)
        self.assertEqual("ms", unit)

    def test_number_to_local_datetime_InMicros(self):
        d = datetimeutil.real_localize(
            datetime.datetime(2016, 3, 12),
            datetimeutil.LOCAL_TIMEZONE,
        )
        ts = datetimeutil.datetime_to_timestamp(d) * 1000000

        guessed_dt, unit = datetimeutil.number_to_local_datetime(ts)
        self.assertEqual(d, guessed_dt)
        self.assertEqual("us", unit)

    def test_number_to_local_datetime_InNanos(self):
        d = datetimeutil.real_localize(
            datetime.datetime(2016, 3, 12),
            datetimeutil.LOCAL_TIMEZONE,
        )
        ts = datetimeutil.datetime_to_timestamp(d) * 1000000000

        guessed_dt, unit = datetimeutil.number_to_local_datetime(ts)
        self.assertEqual(d, guessed_dt)
        self.assertEqual("ns", unit)

    def test_timestamp_regex_ValidTimestamp(self):
        m = datetimeutil.TIMESTAMP_REGEX.search("1457859600")
        self.assertEqual("1457859600", m.group())

    def test_timestamp_regex_ValidTimestampWithPrefix(self):
        m = datetimeutil.TIMESTAMP_REGEX.search("a1457859600")
        self.assertEqual("1457859600", m.group())

    def test_timestamp_regex_ValidTimestampWithSuffix(self):
        m = datetimeutil.TIMESTAMP_REGEX.search("1457859600a")
        self.assertEqual("1457859600", m.group())