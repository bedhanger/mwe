"""Self-tests"""

import pytest
import unittest

from . import LsAttr

class LsAttrTestCase_01(unittest.TestCase):

    def test_general(self):

        # On its own
        X = LsAttr()
        print(X)

        # Single inheritance
        class X(LsAttr):
            pass
        print(X())

        class X(LsAttr):
            def __init__(self):
                self.x = 1
        print(X())

        class X(LsAttr):
            def __init__(self):
                self.x = 1
                self.y = 2
        print(X())

        # Multiple inheritance
        class X(LsAttr, list):
            pass
        print(X())

        class X():
            def __init__(self):
                self.y = None

        class Y(LsAttr, X):
            def __init__(self):
                super().__init__()
                self.z = 'Hi'
        print(Y())

        # Defaults
        class X(LsAttr):
            def __init__(self, a=[]):
                self.a = a
        print(X())
        print(X(a=['b']))

unittest.main(verbosity=3)
