"""Decorate an instance method with pre- and/or postconditions that must be fulfilled

    class C:

        def __init__(self, data=None):
            self.data = data

        @requires(that='self.data is not None')
        @requires(that='self.data == "spam"', when=APRIORI)
        @requires(that='True is not False')
        @requires(that='self.data != "spam"', when=POSTMORTEM)
        @requires(that='len(self.data) >= 3', when=BEFOREANDAFTER)
        def method(self):
            self.data = 'ham'

    X = C(data='spam')
    X.method()

The "that" can be almost any valid Python statement which can be evaluated for its veracity, and
whose result will decide whether or not the method fires.

The parameter "when" decides if the condition is a-priori, post-mortem or before-and-after.
The default is a-priori, meaning a precondition.  Note that before-and-after does *not* mean during;
you cannot mandate an invariant this way!

RequirementNotFulfilledError is the exception you have to deal with in case a condition is not met.
"""
from typing import Optional, Callable
from functools import wraps

from ._when import When, APRIORI, POSTMORTEM, BEFOREANDAFTER
from ._exceptions import RequirementNotFulfilledError

def requires(that, when: When = APRIORI) -> Optional[Callable]:
    """Require <that> of the decoratee, and require it <when>"""

    def func_wrapper(func: Callable) -> Optional[Callable]:
        """First-level wrap the decoratee"""

        @wraps(func)
        def inner_wrapper(self, *pargs, **kwargs) -> Optional[Callable]:
            """Wrap the first-level wrapper

            The wrapping stops here...
            """
            try:
                if when == APRIORI:
                    assert eval(that)
                    # We can use a return here :-)
                    return func(self, *pargs, **kwargs)
                elif when == POSTMORTEM:
                    func(self, *pargs, **kwargs)
                    assert eval(that)
                elif when == BEFOREANDAFTER:
                    assert eval(that)
                    func(self, *pargs, **kwargs)
                    assert eval(that)
                # We don't need an else clause; trying to enlist something that's not in the enum
                # will be penalised with an AttributeError, and small typos will be healed with a
                # suggestion as to what you might have meant.
            except AssertionError as exc:
                raise RequirementNotFulfilledError(that, when) from exc
        return inner_wrapper

    return func_wrapper
