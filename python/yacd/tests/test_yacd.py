#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from yacd import singleton


class TestCase_Singleton:

    def test_non_singletons_are_different(self):

        class C:...

        assert C() is not C()

    def test_singletons_are_equal(self):

        @singleton
        class C:...

        assert C() is C()
