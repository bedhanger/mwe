"""Determine the temperature readings as per the lm sensors package."""

import shutil
import subprocess
import re
import textwrap

class TemperatureReadings:

    def __init__(self) -> None:
        self._sensors = shutil.which('sensors')
        self._tr = None

    def __enter__(self):
        try:
            assert self._sensors is not None
        except AssertionError as exc:
            self._logger.log(logging.ERROR, 'lm sensors package seems missing from system')
            raise FileNotFoundError from exc
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False

    def __call__(self) -> None:
        _sensors = subprocess.check_output(r'sensors').decode()

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

    def __repr__(self) -> object:
        _me = type(self).__name__
        return f"{_me}()"

    def __str__(self) -> str:
        try:
            assert self._tr is not None
        except AssertionError as exc:
            return 'Temperature readings not avalable'
        _pretty = ''
        for _s in self._tr:
            _pretty = _pretty + textwrap.dedent(f"""
                The reading for {_s.group('selector')} is\t{_s.group('values')}
            """).lstrip()
        return _pretty

if __name__ == '__main__':

    with TemperatureReadings() as tr:
        _ = tr()
        print(tr, end='')
