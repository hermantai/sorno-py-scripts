"""Tests for sorno.datetimeutil


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

import datetime
import re
import time
import unittest

from sorno import datetimeutil
import pytz


_LOCAL_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
_LOCAL_TIMESTAMP_FOR_GO_REFERENCE_TIME = (
    datetimeutil.GO_REFERENCE_TIME.astimezone(
        datetimeutil.LOCAL_TIMEZONE
    ).strftime(
        _LOCAL_TIMESTAMP_FORMAT
    )
)


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

    def test_datetime_to_timestamp_differentTimeZone(self):
        mst_dt = datetimeutil.GO_REFERENCE_TIME
        los_angeles_dt = datetimeutil.convert_timezone(
            mst_dt,
            self.los_angeles_time_zone,
        )
        self.assertEqual(
            datetimeutil.datetime_to_timestamp(mst_dt),
            datetimeutil.datetime_to_timestamp(los_angeles_dt),
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

    def test_guess_local_datetime_invalidString(self):
        s = "abc"
        try:
            datetimeutil.guess_local_datetime(s)
            self.fail("%s should not be a valid date time", s)
        except ValueError:
            pass

    def test_guess_local_datetime_isoFormat(self):
        s = "2006-01-02T15:04:05-0700"
        dt = datetimeutil.guess_local_datetime(s)
        self.assertEqual(
            _LOCAL_TIMESTAMP_FOR_GO_REFERENCE_TIME,
            dt.strftime(_LOCAL_TIMESTAMP_FORMAT),
        )

    def test_guess_local_datetime_isoDateFormat(self):
        s = "2006-01-02"
        dt = datetimeutil.guess_local_datetime(s)
        self.assertEqual(
            "2006-01-02 00:00:00",
            dt.strftime(_LOCAL_TIMESTAMP_FORMAT),
        )

    def test_guess_local_datetime_isoFormatWithZ(self):
        s = "2006-01-02T15:04:05Z"
        dt = datetimeutil.guess_local_datetime(s)
        self.assertEqual(
            "2006-01-02 07:04:05",
            dt.strftime(_LOCAL_TIMESTAMP_FORMAT),
        )

    def test_strftime(self):
        # convert go time to local timezone first
        dt = datetimeutil.GO_REFERENCE_TIME.astimezone(
            datetimeutil.LOCAL_TIMEZONE
        )
        result_from_dt = datetimeutil.strftime(
            datetimeutil.ISO_FORMAT,
            dt,
        )

        result_from_ts = datetimeutil.strftime(
            datetimeutil.ISO_FORMAT,
            time.mktime(dt.timetuple()),
        )
        result_from_struct_time = datetimeutil.strftime(
            datetimeutil.ISO_FORMAT,
            dt.timetuple(),
        )

        self.assertEqual(result_from_dt, result_from_ts)
        self.assertEqual(result_from_ts, result_from_struct_time)
