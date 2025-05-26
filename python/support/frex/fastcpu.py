import textwrap
from typing import Self

from support.lsattr import LsAttr

class FastCpu(LsAttr):

    """Model a CPU that runs fast(er than the min frex)."""

    def __init__(self, identity: int, model: str, mhz: float) -> None:
        self.identity = identity
        self.model = model
        self.mhz = mhz
        self.governor = None

    def __str__(self) -> str:
        """Pretty-print."""
        return textwrap.dedent(f"""
            Processor id  : {self.identity}
            Model name    : {self.model}
            Speed in MHz  : {self.mhz}
            Frex governor : {self.governor}
        """).lstrip()

    def __enter__(self) -> Self:
        """Complete the CPU by determining its frex governor."""
        self.governor = hex(id(self))
        return self

    def __exit__(self, exc_value, exc_type, traceback) -> bool:
        """Bye."""
        return False
