"""Simple wrapper for getting the number of CPUs in the system."""

from multiprocessing import cpu_count as nproc
from typing import Self

class NProc:
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

        # Sanity checks
        assert self._cpu_count is not None, 'Could not determine number of CPUs'
        assert self._cpu_count > 0, 'Uh, *what* am i running on?!?'

        return self._cpu_count

if __name__ == '__main__':

    x = NProc()
    print(x)
    print(x())

    with NProc() as y:
        print(y)
        print(y())

    assert x != y
    assert x() == y()
