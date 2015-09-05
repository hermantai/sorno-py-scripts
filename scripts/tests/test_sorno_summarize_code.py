"""
Unit test for sorno_summarize_code.

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

import unittest

from sorno_summarize_code import PythonFileSummarizer


class PythonFileSummarizerTestCase(unittest.TestCase):
    def setUp(self):
        self.summarizer = PythonFileSummarizer()

    def test_summarize_SimpleFunction(self):
        code = """
def f1(a, b, c, d=None, **kwargs):
    pass
"""
        self._print_header(code)
        self.summarizer.summarize(code)

    def test_summarize_FunctionSpanMoreThanOneLine(self):
        code = """
def f1(
    a
):
    pass
"""
        self._print_header(code)
        self.summarizer.summarize(code)

    def test_summarize_ClassWithOneFunc(self):
        code = """
class MyClass(object):
    def f1(a, b, c, d=None, **kwargs):
        pass
"""
        self._print_header(code)
        self.summarizer.summarize(code)

    def _print_header(self, code_input):
        print("{0:=^40}".format(" input "))
        print(code_input)
        print("{0:=^40}".format(" output "))


if __name__ == '__main__':
    unittest.main(verbosity=0)
