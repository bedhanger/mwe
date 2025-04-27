"""Determine the temperature readings as per the lm sensors package."""

import shutil
import subprocess
import re
import textwrap
import logging
import pytest

class TemperatureReadings:

    def __init__(self, auto_read=True) -> None:
        self._sensors = shutil.which('sensors')
        self._tr = None
        self._auto_read = auto_read
        self._logger = logging.getLogger()

    def __enter__(self):
        try:
            assert self._sensors is not None
        except AssertionError as exc:
            self._logger.log(logging.ERROR, 'lm sensors package seems missing from system')
            raise FileNotFoundError('Please install the lm sensors package') from exc
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False

    def __call__(self) -> None:
        """Inspect the sensors output to find temperature matches.

        Care about values for CPU and motherboard.
        """

        _sensors = subprocess.check_output(self._sensors).decode()
        _temps_rx = re.compile(r'''
            (?P<selector>(CPU|MB))
            \s
            Temperature
            \s*
            :
            \s+
            (?P<values>.+)
            ''', re.VERBOSE)
        self._tr = re.finditer(_temps_rx, _sensors)

    def __iter__(self):
        """Arm and return an iterator for the raw matches."""
        if self._auto_read:
            self.__call__()
        return self._tr

    def __repr__(self) -> object:
        _me = self.__class__.__name__
        return f"{_me}()"

    def __str__(self) -> str:
        if self._auto_read:
            self.__call__()
        try:
            assert self._tr is not None
        except AssertionError as exc:
            return 'Temperature readings are not (yet?) available'

        # Unwind the iterator
        _pretty = ''
        for _s in self._tr:
            _pretty = _pretty + textwrap.dedent(f"""
                The temperature reading for the {_s.group('selector')} is\t{_s.group('values')}
            """).lstrip()
        return _pretty.strip()

if __name__ == '__main__':

    with TemperatureReadings() as tr:

        # Id ourselves
        print(repr(tr))

        # Pretty-print results
        print(tr)

        # You can iterate over the raw reading matches if you like
        for i in tr:
            print(i)

    # Now prepare everything, but don't actually read the values
    with TemperatureReadings(auto_read=False) as tr:

        # Id ourselves
        print(repr(tr))

        # Pretty-print "results"
        print(tr)

        # You cannot iterate over the raw reading matches unless you perform the reading yourself
        with pytest.raises(TypeError):
            for i in tr:
                print(i)

        # Once you do, you can
        tr()
        for i in tr:
            print(i)

        # But the results are empty
        assert str(tr) == ''

        # Until you do another reading
        tr()
        assert str(tr) != ''
