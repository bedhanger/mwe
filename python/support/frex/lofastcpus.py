import textwrap
from typing import Iterator, Self

from support.lsattr import LsAttr
from .fastcpu import FastCpu

class ListOfFastCpus(LsAttr):

    """Collect fast CPUs."""

    def __init__(self, fastcpus=[]) -> None:
        self.fastcpus = fastcpus

    def __str__(self) -> str:
        """Pretty-print."""

        if len(self.fastcpus) == 0:
            return 'The are currently no fast CPUs known...'
        return str('-' * 80 + '\n').join(str(_fastcpu) for _fastcpu in self).rstrip()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_value, exc_type, traceback) -> bool:
        """Bye."""
        return False

    def __add__(self, another):
        self.fastcpus.append(another)
        return self.__class__(fastcpus=self.fastcpus)

    def __iter__(self) -> Iterator[list]:
        for i in self.fastcpus:
            yield i

    def __len__(self) -> int:
        return len(self.fastcpus)

if __name__ == '__main__':

    with ListOfFastCpus() as f:
        print(repr(f))
        print(f)
        print('Total:', len(f))

        with FastCpu(identity=42, model='Alpha', mhz=1) as g:
            with FastCpu(identity=4711, model='HP', mhz=1000) as h:
                i = FastCpu(identity=123, model='Turing Machine', mhz=300)
                j = FastCpu(identity=321, model='Abakus', mhz=9)
                # Note that the fast CPUs not introduced via a context, won't have their frex
                # governor set.  It pays to use contexts whenever possible.
                f = f + g + h + i + j

                print(repr(f))
                print(f)
                print('Total:', len(f))

                with ListOfFastCpus(fastcpus=[g, h, i, j, j, i, h, g]) as k:
                    print(repr(k))
                    print(k)
                    print('Total:', len(k))
