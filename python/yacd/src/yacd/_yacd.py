"""Motley of decorators, some of which tend to limit things

Study the test code to see example usages.
"""
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
