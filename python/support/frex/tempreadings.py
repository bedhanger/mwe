"""Determine the temperature readings as per the lm sensors package."""

import shutil
import subprocess
import re
import textwrap
import logging
import pytest
from typing import Iterator, Self

from support.lsattr import LsAttr

class TemperatureReadings(LsAttr):

    def __init__(self, auto_read=True) -> None:
        self._sensors = shutil.which('sensors')
        self._tr = None
        self._auto_read = auto_read
        self._logger = logging.getLogger()

    def __enter__(self) -> Self:
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

    def __iter__(self) -> Iterator[re.Match]:
        """Arm and return an iterator for the raw matches."""
        if self._auto_read:
            self.__call__()
        for _raw_match in self._tr:
            yield _raw_match

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
