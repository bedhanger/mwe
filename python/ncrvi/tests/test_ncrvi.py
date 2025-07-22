#!/usr/bin/env --split-string=python -m pytest --verbose

"""Self test code"""

import pytest

from ncrvi import main

class Testcase_Providers_01:

    def test_generals(self):

        assert 1 == 1
