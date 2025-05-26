"""Unit tests"""

import unittest
import pytest

from . import FastCpu

class FastCpuTestCase(unittest.TestCase):

    def test_general(self):

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

        print(repr(q))

unittest.main(verbosity=3)
