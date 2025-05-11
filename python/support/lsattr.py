#!/usr/bin/env python

class LsAttr:

    def __lsattr(self):
        return ', '.join(f'{attr}={self.__dict__[attr]!r}' for attr in sorted(self.__dict__))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__lsattr()})'

if __name__ == '__main__':

    X = LsAttr()
    print(X)

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

    class X(LsAttr):
        def __init__(self, a=[]):
            self.a = a
    print(X())
    print(X(a=['b']))
