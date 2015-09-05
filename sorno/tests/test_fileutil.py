"""Tests for sorno.fileutil


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

import inspect
import unittest


from sorno import fileutil

class FileUtilTestCase(unittest.TestCase):
    FILEPATH_PREFIX = "/tmp/FileUtilTestCase_"

    def test_is_text_file_TextFile_True(self):
        filepath = self._get_file_path()
        with open(filepath, "w") as f:
            f.write("abc")

        self.assertTrue(fileutil.is_text_file(filepath))

    def test_is_text_file_BinaryFile_False(self):
        filepath = self._get_file_path()
        with open(filepath, "wb") as f:
            f.write("\a\0")

        self.assertFalse(fileutil.is_text_file(filepath))

    def _get_file_path(self):
        return self.FILEPATH_PREFIX + inspect.stack()[1][3]



if __name__ == '__main__':
    unittest.main()
