#!/usr/bin/env --split-string=pytest --verbose

"""Self-test code"""

import pytest

from runmwe import MweRunner
from support.ooce.exceptions import OutOfContextError

def test_context_based_usage():

    with MweRunner() as R:
        R()
        print(repr(R))
        print(R)

def test_contextless_usage():

    R = MweRunner()
    with pytest.raises(OutOfContextError):
        R()

    with pytest.raises(OutOfContextError):
        print(R)

def test_legal_contextless_usage():

    R = MweRunner()
    # This can be called outwith a context
    print(repr(R))
