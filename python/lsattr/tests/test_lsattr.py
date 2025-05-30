#!/usr/bin/env --split-string=python -m pytest --verbose

"""Self-tests"""
import pytest

from lsattr import LsAttr

def test_general():
    X = LsAttr()
    assert repr(X) == 'LsAttr()'

def test_single_inheritance():
    class X(LsAttr):
        pass
    assert repr(X()) == 'X()'

    class X(LsAttr):
        def __init__(self):
            self.x = 1
    assert repr(X()) == 'X(x=1)'

    class X(LsAttr):
        def __init__(self):
            self.x = 1
            self.y = 2
    assert repr(X()) == 'X(x=1, y=2)'

def test_multiple_inheritance():
    class X(LsAttr, list):
        pass
    assert repr(X()) == 'X()'

    class X():
        def __init__(self):
            self.y = None
    assert repr(X()) != 'X()' # !!!

    class Y(LsAttr, X):
        def __init__(self):
            super().__init__()
            self.z = 'Hi'
    assert repr(Y()) == "Y(y=None, z='Hi')"

def test_defaults():
    class X(LsAttr):
        def __init__(self, a=[]):
            self.a = a
    assert repr(X()) == "X(a=[])"
    assert repr(X(a=['b'])) == "X(a=['b'])"
