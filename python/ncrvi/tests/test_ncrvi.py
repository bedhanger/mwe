#!/usr/bin/env --split-string=python -m pytest --verbose

"""Implement the tests"""

import pytest
import random
import time
import os

class TestCase_Ncrvi:

    POWER_ON_WAIT = float(os.environ['POWER_ON_WAIT'])
    POWER_OFF_WAIT = float(os.environ['POWER_OFF_WAIT'])
    SETTLING_DELAY = float(os.environ['SETTLING_DELAY'])
    EXPECTED_COMPONENTS = int(os.environ['EXPECTED_COMPONENTS'])
    HOW_OFTEN = int(os.environ['HOW_OFTEN'])

    @pytest.fixture
    def total_components(self) -> int:

        time.sleep(self.POWER_OFF_WAIT)
        print('Power off')
        time.sleep(self.POWER_ON_WAIT)
        print('Power on')
        time.sleep(self.SETTLING_DELAY)
        print('Work')
        time.sleep(self.POWER_OFF_WAIT)
        print('Power off')

        yield random.choice(range(self.EXPECTED_COMPONENTS))

    @pytest.mark.parametrize('how_often', range(HOW_OFTEN))
    def test_it(self, total_components, how_often):

        assert total_components == self.EXPECTED_COMPONENTS - 1
