#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest

from nproc import NProc

class TestCaseNProc_01:

    def test_has_a_cpu(self):
        assert NProc() is not None, 'Could not determine number of CPUs'
        assert NProc()() > 0, 'Uh, *what* am i running on?!?'

    def test_is_multiprocessing(self):
        with NProc() as n:
            assert n() > 1

    def test_general(self):
        x = NProc()

        with NProc() as y:
            assert x != y
            assert x() == y()
