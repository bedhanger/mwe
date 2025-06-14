"""Decorate an instance method with pre- and/or postconditions that must be fulfilled

    class C:

        def __init__(self, data=None):
            self.data = data

        @requires(that='self.data is not None')
        @requires(that='self.data == "spam"', when='a-priori')
        @requires(that='True is not False')
        @requires(that='self.data != "spam"', when='post-mortem')
        def method(self):
            self.data = 'ham'

    X = C(data='spam')
    X.method()

The "that" can be almost any valid Python statement which can be evaluated for its veracity, and
whose result will decide whether or not the method fires.

The parameter "when" decides if the condition is a-priori or post-mortem.  The default is a-priori,
meaning a precondition.  ValueError is raised if you specify anything else.

RequirementNotFulfilledError is the exception you have to deal with in case a condition is not met.
"""
from typing import Optional, Callable
from functools import wraps

class RequirementNotFulfilledError(Exception):
    """Raise this when a requirement is found wanting"""
    pass

def requires(that, when: str = 'a-priori') -> Optional[Callable]:
    """Require <that> of the decoratee, and require it <when>"""

    def func_wrapper(func: Callable) -> Optional[Callable]:
        """First-level wrap the decoratee"""

        @wraps(func)
        def inner_wrapper(self, *pargs, **kwargs) -> Optional[Callable]:
            """Wrap the first-level wrapper

            The wrapping stops here...
            """
            try:
                if when == 'a-priori':
                    assert eval(that)
                    return func(self, *pargs, **kwargs)
                elif when == 'post-mortem':
                    func(self, *pargs, **kwargs)
                    assert eval(that)
                else:
                    raise ValueError(f'{when!r} is not a valid condition indicator')
            except AssertionError as exc:
                raise RequirementNotFulfilledError(f'{that!r} ({when}) does not hold') from exc
        return inner_wrapper

    return func_wrapper
