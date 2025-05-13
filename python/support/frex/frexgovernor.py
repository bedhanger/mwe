"""Determine a CPU's frequency governor."""

import pytest
from pathlib import Path
import textwrap

from support.lsattr import LsAttr

class FrexGovernor(LsAttr):

    def __init__(self, of_cpu: str='cpu0') -> None:
        self._of_cpu = of_cpu
        self._fg = None

    def __enter__(self):
        self._gov_file = (
            Path('/sys/devices/system/cpu') /
            Path(self._of_cpu.lower()) /
            Path('cpufreq/scaling_governor')
        )
        assert self._gov_file.exists(), 'Cannot find file containing CPU governor'
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        return False

    def __call__(self) -> str:
        with open(self._gov_file) as f:
            self._fg = f.readline().rstrip()
        assert self._fg is not None, 'Cannot determine frequency governor'
        return self._fg

    def __str__(self) -> str:
        return textwrap.dedent(f"""
            {self._of_cpu} says its frequency governor is "{self._fg}".
        """).strip()

if __name__ == '__main__':

    with FrexGovernor() as f:
        x = f()
        assert isinstance(x, str), 'Cannot interpret frequency governor'

    with FrexGovernor('cpu11') as f:
        x = f()
        print(x)

    with FrexGovernor(of_cpu='CPU8') as f:
        print(f)
        f()
        print(f)

    with FrexGovernor(of_cpu='cpu9') as f:
        print(f())

    with FrexGovernor(of_cpu='CpU3') as f:
        print(f())

    # Not adhering to the context manager protocol does not work
    with pytest.raises(AttributeError):
        y = FrexGovernor(of_cpu='cpu2')
        y = y()
        print(y)

    with pytest.raises(AssertionError):
        with FrexGovernor(of_cpu='no such cpu') as f:
            pass
