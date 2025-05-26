"""Unit tests"""

import unittest
import textwrap
import pytest

from . import FastCpu

class FastCpuTestCase(unittest.TestCase):

    def test_general(self):

        X = FastCpu(42, 'Alpha', 300)
        Y = FastCpu(22, 'Vax', 30)

        assert str(X).lstrip() == textwrap.dedent(f'''
            Processor id  : 42
            Model name    : Alpha
            Speed in MHz  : 300
            Frex governor : None
        ''').lstrip()

        assert str(Y).lstrip() == textwrap.dedent(f'''
            Processor id  : 22
            Model name    : Vax
            Speed in MHz  : 30
            Frex governor : None
        ''').lstrip()

        Z = []
        Z.append(X)
        Z.append(Y)

        with FastCpu(identity=123.3, model='Turing Machine', mhz=1) as q:
            Z.append(q)

            assert len(Z) == 3

            assert repr(q) == f"FastCpu(governor={hex(id(q))!r}, identity=123.3, mhz=1, model='Turing Machine')"
            assert str(q).lstrip() == textwrap.dedent(f'''
                Processor id  : 123.3
                Model name    : Turing Machine
                Speed in MHz  : 1
                Frex governor : {hex(id(q))}
            ''').lstrip()

unittest.main(verbosity=3)
