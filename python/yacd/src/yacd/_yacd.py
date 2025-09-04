#!/usr/bin/env python

from functools import wraps


def singleton(class_):
    """Make a class a singleton as per

        https://realpython.com/primer-on-python-decorators/#creating-singletons
    """
    @wraps(class_)
    def __wrapper(*pargs, **kwargs):

        if __wrapper.instance is None:
            __wrapper.instance = class_(*pargs, **kwargs)
        return __wrapper.instance

    __wrapper.instance = None
    return __wrapper


def nullfiy(callable_):
    """Make a callable's code ineffective"""

    @wraps(callable_)
    def __wrapper(*pargs, **kwargs) -> None:

        return None

    return __wrapper


def callify(instance):
    """Equate an instance with its __call__ method's return"""

    @wraps(instance)
    def __wrapper(*pargs, **kwargs):

        return instance(*pargs, **kwargs)

    return __wrapper


def instancify(cls=None, /, *pargs, **kwargs):
    """Equate a class with an instance of it"""

    def __instancify(cls, *pargs, **kwargs):
        return cls(*pargs, **kwargs)

    def wrap(cls):
        return __instancify(cls, *pargs, **kwargs)

    if cls is None:
        return wrap

    return wrap(cls)
