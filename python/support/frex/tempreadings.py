"""Determine the temperature readings as per the lm sensors package."""

import shutil
import subprocess
import re
import textwrap
import logging

class TemperatureReadings:

    def __init__(self) -> None:
        self._sensors = shutil.which('sensors')
        self._tr = None
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

    def __call__(self) -> iter:
        """Inspect the sensors output to find temperature matches.

        Care about values for CPU and motherboard.
        Return them as an iterator.
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
        return self._tr

    def __repr__(self) -> object:
        _me = type(self).__name__
        return f"{_me}()"

    def __str__(self) -> str:
        try:
            assert self._tr is not None
        except AssertionError as exc:
            return 'Temperature readings not available'

        # Unwind the iterator
        _pretty = ''
        for _s in self._tr:
            _pretty = _pretty + textwrap.dedent(f"""
                The temperature reading for the {_s.group('selector')} is\t{_s.group('values')}
            """).lstrip()
        return _pretty.strip()

if __name__ == '__main__':

    with TemperatureReadings() as tr:
        print(tr)
        temperature_readings = tr()
        print(tr)

        # You can iterate over the reading matches if you like...(need to rewind the iterator)
        temperature_readings = tr()
        for i in temperature_readings:
            print(i)
