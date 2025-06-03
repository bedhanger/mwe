#!/usr/bin/env --split-string=python -m pytest --verbose

"""Self-test code"""

import pytest
from typing import Iterator

from runmwe import MweRunner
from ooce.exceptions import OutOfContextError

@pytest.fixture
def contextless_runner() -> Iterator[MweRunner]:
    R = MweRunner()
    yield R

@pytest.fixture
def contextful_runner() -> Iterator[MweRunner]:
    with MweRunner() as R:
        yield R

class TestCaseMweRunner_01:

    def test_context_based_usage(self, contextful_runner):

        contextful_runner()
        print(repr(contextful_runner))
        print(contextful_runner)
        contextful_runner

    def test_contextless_usage(self, contextless_runner):

        with pytest.raises(OutOfContextError):
            contextless_runner()

        contextless_runner

        with pytest.raises(OutOfContextError):
            print(contextless_runner)

    def test_legal_contextless_usage(self, contextless_runner, contextful_runner):

        # This can be called outwith a context or within
        print(repr(contextless_runner))
        print(repr(contextful_runner))
        contextless_runner
