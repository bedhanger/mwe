#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

import dice

class TestCaseDice_01:

    def test_general(self):

        Bad = False
        assert not Bad
