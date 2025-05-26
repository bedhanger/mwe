"""Unit tests"""

import unittest
import pytest

from . import FastCpu

class FastCpuTestCase(unittest.TestCase):

    def test_general(self):

        X = FastCpu(42, 'Alpha', 300)
        Y = FastCpu(22, 'Vax', 30)

        Z = []
        Z.append(X)
        Z.append(Y)
        with FastCpu(identity=123.3, model='Turing Machine', mhz=1) as q:
            Z.append(q)

        assert len(Z) == 3
        print('-' * 100)
        for p in Z:
            print(p, end='-' * 100 + '\n')

        assert repr(q) == f"FastCpu(governor={hex(id(q))!r}, identity=123.3, mhz=1, model='Turing Machine')"

unittest.main(verbosity=3)
