#!/usr/bin/env --split-string=python -m pytest --verbose

"""Self-test code"""

import pytest

from runmwe import MweRunner
from ooce.exceptions import OutOfContextError

class TestCaseMweRunner_01:

    def test_context_based_usage(self):

        with MweRunner() as R:
            R()
            print(repr(R))
            print(R)

    def test_contextless_usage(self):

        R = MweRunner()
        with pytest.raises(OutOfContextError):
            R()

        with pytest.raises(OutOfContextError):
            print(R)

    def test_legal_contextless_usage(self):

        R = MweRunner()
        # This can be called outwith a context
        print(repr(R))
