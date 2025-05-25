"""Determine the minimum CPU frequency this is running on."""

import pytest
from pathlib import Path
import textwrap
from typing import Self

from support.lsattr import LsAttr

class MinFrequency(LsAttr):

    def __init__(self, ref_cpu: str='cpu0') -> None:
        self._ref_cpu = ref_cpu
        self._mf = None

    def __enter__(self) -> Self:
        self._min_frex_file = (
            Path('/sys/devices/system/cpu') /
            Path(self._ref_cpu.lower()) /
            Path('cpufreq/cpuinfo_min_freq')
        )
        assert self._min_frex_file.exists(), 'Cannot find file containing minimum CPU frequency'
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False

    def __call__(self) -> float:
        with open(self._min_frex_file) as f:
            self._mf = float(f.readline().rstrip())
        assert self._mf is not None, 'Cannot determine minimum frequency'
        return self._mf

    def __str__(self) -> str:
        assert self._mf is not None, 'Ups, no-one has tried to determine the min frex'
        return textwrap.dedent(f"""
            The minimum frequency is {self._mf / 1000.0} MHz, according to {self._ref_cpu}.
        """).strip()

if __name__ == '__main__':

    with MinFrequency() as m:
        x = m()
        assert isinstance(x, float), 'Cannot interpret frequency as a float'

    with MinFrequency('cpu11') as m:
        x = m()
        print(x)

    with MinFrequency(ref_cpu='CPU7') as m:
        m()
        print(m)

    with MinFrequency(ref_cpu='cpu9') as m:
        print(m())

    with MinFrequency(ref_cpu='CpU3') as m:
        print(m())

    with pytest.raises(AssertionError):
        with MinFrequency(ref_cpu='no such cpu') as m:
            pass
