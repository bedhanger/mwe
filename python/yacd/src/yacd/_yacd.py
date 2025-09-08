"""Motley of decorators, some of which tend to limit things

Study the test code to see example usages.
"""
from functools import wraps


class singleton:
    """Make a class a singleton, loosely based on

        https://realpython.com/primer-on-python-decorators/#creating-singletons
    """
    def __init__(self, class_):
        self.class_ = class_
        self.instance = None

    def __call__(self, *pargs, **kwargs):
        if self.instance is None:
            self.instance = self.class_(*pargs, **kwargs)
        return self.instance


def nullfiy(callable_):
    """Make a callable's code ineffective"""

    @wraps(callable_)
    def __wrapper(*pargs, **kwargs) -> None:

        return None

    return __wrapper


def callify(instance=None, /, *pargs, **kwargs):
    """Equate an instance with the return of its __call__ routine

    It is, essentially, like instancify
    """
    def __callify(instance, *pargs, **kwargs):
        return instance(*pargs, **kwargs)

    @wraps(instance)
    def wrap(instance):
        return __callify(instance, *pargs, **kwargs)

    # @callify()
    if instance is None:
        return wrap

    # @callify
    return wrap(instance)


def instancify(cls=None, /, *pargs, **kwargs):
    """Equate a class with an instance of it

    It is, essentially, like callify.
    """
    def __instancify(cls, *pargs, **kwargs):
        return cls(*pargs, **kwargs)

    @wraps(cls)
    def wrap(cls):
        return __instancify(cls, *pargs, **kwargs)

    # @instancify()
    if cls is None:
        return wrap

    # @instancify
    return wrap(cls)
