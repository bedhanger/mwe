import textwrap

class FastCpu:

    """Model a CPU that runs fast(er than the min frex)."""

    def __init__(self, identity: int, model: str, mhz: float) -> None:
        self._identity = identity
        self._model = model
        self._mhz = mhz
        self._governor = None

    def __repr__(self) -> object:
        """Unambiguously represent."""
        _me = type(self).__name__
        return  f"{_me}(identity={self._identity!r}, model={self._model!r}, mhz={self._mhz!r})"

    def __str__(self) -> str:
        """Pretty-print."""
        return textwrap.dedent(f"""
            Processor id  : {self._identity}
            Model name    : {self._model}
            Speed in MHz  : {self._mhz}
            Frex governor : {self._governor}
        """).lstrip()

    def __enter__(self):
        """Complete the CPU by determining its frex governor."""
        self._governor = hex(id(self))
        return self

    def __exit__(self, exc_value, exc_type, traceback) -> bool:
        """Bye."""
        return False

if __name__ == '__main__':
    """Test the above."""
    X = FastCpu(42, 'Alpha', 300)
    Y = FastCpu(22, 'Vax', 30)

    Z = []
    Z.append(X)
    Z.append(Y)
    with FastCpu(identity=123.3, model='Turing Machine', mhz=1) as q:
        Z.append(q)

    print('I see', len(Z), 'fast CPUs, namely:')
    print('-' * 100)
    for p in Z:
        print(p, end='-' * 100 + '\n')

    print(Z)
