"""Simple wrapper for getting the number of CPUs in the system."""

from multiprocessing import cpu_count as nproc
from typing import Self

from lsattr import LsAttr

class NProc(LsAttr):
    """Mimic the nproc command."""

    def __init__(self) -> None:
        self._cpu_count = None

    def __enter__(self) -> Self:
        self._cpu_count = 0
        return self

    def __exit__(self, exc_value, exc_type, traceback) -> bool:
        return False

    def __call__(self) -> int:
        self._cpu_count = nproc()

        return self._cpu_count
