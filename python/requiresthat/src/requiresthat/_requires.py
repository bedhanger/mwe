"""Decorate an instance method with preconditions that must be fulfilled for it to be runnable

    class C:

        def __init__(self, data):
            self.data = data

        @requires(that='self.data is not None')
        @requires(that='True is not False')
        def method(self): ...

    X = C()
    X.run()

The "that" can be almost any valid Python statement which can be evaluated for its veracity, and
whose result will decide whether or not the method fires.

RequirementNotFulfilledError is the exception you have to deal with in case a precondition is not
met.
"""
from typing import Optional, Callable
from functools import wraps

class RequirementNotFulfilledError(Exception):
    """Raise this when a requirement is found wanting"""
    pass

def requires(that) -> Optional[Callable]:
    """Require <that> of the decoratee"""

    def func_wrapper(func: Callable) -> Optional[Callable]:
        """First-level wrap the decoratee"""

        @wraps(func)
        def inner_wrapper(self, *pargs, **kwargs) -> Optional[Callable]:
            """Wrap the first-level wrapper

            The wrapping stops here...
            """
            try:
                assert eval(that)
                return func(self, *pargs, **kwargs)
            except AssertionError as exc:
                raise RequirementNotFulfilledError(f'{that!r} does not hold') from exc
        return inner_wrapper

    return func_wrapper
