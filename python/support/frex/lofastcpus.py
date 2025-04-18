import textwrap

from .fastcpu import FastCpu

class ListOfFastCpus():

    """Collect fast CPUs."""

    def __init__(self, fastcpus=[]) -> None:
        self._fastcpus = fastcpus

    def __repr__(self) -> object:
        """Unambiguously represent."""
        _me = type(self).__name__
        return  f"{_me}(fastcpus={self._fastcpus!r})"

    def __str__(self) -> str:
        """Pretty-print."""

        if len(self._fastcpus) == 0:
            return 'The are currently no fast CPUs known...'
        _fastcpu = iter(self)
        _str = ''
        try:
            while True:
                _str = _str + str(next(_fastcpu))
        except StopIteration:
            pass
        return _str.rstrip()

    def __enter__(self):
        return self

    def __exit__(self, exc_value, exc_type, traceback) -> bool:
        """Bye."""
        return False

    def __add__(self, another):
        self._fastcpus.append(another)
        return ListOfFastCpus(fastcpus=self._fastcpus)

    def __iter__(self) -> object:
        for i in self._fastcpus:
            yield i

    def __len__(self) -> int:
        return len(self._fastcpus)

if __name__ == '__main__':

    with ListOfFastCpus() as f:
        print(f)

        with FastCpu(identity=42, model='Alpha', mhz=1) as g:
            with FastCpu(identity=4711, model='HP', mhz=1000) as h:
                i = FastCpu(identity=123, model='Turing Machine', mhz=300)
                j = FastCpu(identity=321, model='Abakus', mhz=9)
                # Note that the fast CPUs not introduced via a context, won't have their frex
                # governor set.  It pays to use contexts whenever possible.
                f = f + g + h + i + j
        print(f)
        print(len(f))
