"""Allow decorators of the form

    @requires(that='<some condition be true>')

to be associated with instance methods of a class.

'some condition be true' can be almost any valid Python statement which can be evaluated for its
truth value, and whose result will decide whether or not the method fires.
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
