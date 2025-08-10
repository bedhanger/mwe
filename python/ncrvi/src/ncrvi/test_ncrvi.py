#!/usr/bin/env --split-string=python -m pytest --verbose

"""Implement the tests"""

import pytest
import random
import time
import os
import textwrap
import re

from .command import Command

class TestCase_Ncrvi:

    POWER_ON_WAIT = float(os.environ['POWER_ON_WAIT'])
    INITIAL_WAIT = float(os.environ['INITIAL_WAIT'])
    POWER_OFF_WAIT = float(os.environ['POWER_OFF_WAIT'])
    SETTLING_DELAY = float(os.environ['SETTLING_DELAY'])
    EXPECTED_COMPONENTS = int(os.environ['EXPECTED_COMPONENTS'])
    HOW_OFTEN = int(os.environ['HOW_OFTEN'])
    USER = os.environ['USER']
    TARGET = os.environ['TARGET']

    power_on_cmd = Command('ls', '-la')
    power_off_cmd = Command('df')
    ncrvi_cmd = Command('fortune', '-n25', '-s')

    class NumberOfComponentsError(ArithmeticError): pass
    class ComponentNotFoundError(LookupError): pass
    class NothingToBeDoneError(ValueError): pass

    def test_initial_wait(self):
        """Perform an initial wait to "warm up" the target"""

        try:
            assert self.INITIAL_WAIT
            time.sleep(self.INITIAL_WAIT)
            _ = self.power_on_cmd()
        except AssertionError:
            pytest.skip('Not requested')

    @pytest.fixture
    def the_data(self) -> str:
        """Produce the data to be inspected

        Note that what is returned is only generally checked (for being something rather than
        nothing).  We store the relevant info in an attribute for the other checks to access.

        :returns: the data
        """
        self.the_data_to_check = self.ncrvi_cmd()
        return self.the_data_to_check

    def total_ncrvi(self) -> int:
        """Determine the number of components returning version info

        :returns: The number of such components
        """
        ncrvi_out = 'Hi a dude: ' + str(len(self.the_data_to_check))

        ncrvi_rx = re.compile(r'''
            ^
            \s*
            (?P<intro>
                Hi
                \s
                (a\s)? # Maybe the typo will get fixed one day
                dude
                :
            )
            \s+
            (?P<ncrvi>
                \d+ # That's what we want
            )
            \s*
            $
        ''', re.VERBOSE)
        return int(ncrvi_rx.match(ncrvi_out).group('ncrvi'))

    def is_present(self, component: str = str()) -> re.Match:
        """Determine if a given component is present

        :param component: A string identifying a component
        :returns: A regex match object if the component could be found; None if not
        """
        component = re.compile(f'{component}', re.IGNORECASE)
        return component.search(self.the_data_to_check)

    @pytest.mark.parametrize('how_often', range(1, HOW_OFTEN + 1))
    def test_it(self, the_data, how_often):
        """Perform the ncrvi test a couple of times

        :param the_data: What to look at
        :param how_often: Repeat the experiment this many times
        """
        time.sleep(self.POWER_OFF_WAIT)
        _ = self.power_off_cmd()
        time.sleep(self.POWER_ON_WAIT)
        _ = self.power_on_cmd()
        time.sleep(self.SETTLING_DELAY)

        try:
            # There must be something to do
            try:
                assert the_data is not None
            except AssertionError as exc:
                raise self.NothingToBeDoneError('there is nothing to do?!?')

            # The overall number must match
            total_ncrvi = self.total_ncrvi()
            try:
                assert total_ncrvi == self.EXPECTED_COMPONENTS
            except AssertionError as exc:
                raise self.NumberOfComponentsError(textwrap.dedent(f'''
                    {total_ncrvi!r} ({self.EXPECTED_COMPONENTS!r} expected)
                ''').strip()) from exc

            # Individual components must be present
            try:
                for component in [' ', 'the', 'is']:
                    assert self.is_present(component)
            except AssertionError as exc:
                raise self.ComponentNotFoundError(f'component {component!r} not found') from exc
        except:
            raise
        finally:
            time.sleep(self.POWER_OFF_WAIT)
            _ = self.power_off_cmd()
