#!/usr/bin/env python
"""Base class for runners in MWE."""

import logging
from typing import Callable
from functools import wraps
import textwrap

from support.lsattr import LsAttr

class OutOfContextError(RuntimeError):
    """Raise this when we detect that an out-of-context operation is attempted"""

    pass

class MweRunner(LsAttr):
    """A context-aware runner from which others may be instantiated from."""

    def __new__(cls, *pargs, **kwargs):
        """Make a runner."""
        return super().__new__(cls)

    def __init__(self):
        """Init a newly made runner."""
        # Simplistic form of protection against not instigating the context manager protocol
        self._ctx = None
        self._logger = logging.getLogger()

    def __enter__(self):
        """Establish context.

        Appease the context sentry.
        """
        self._ctx = not None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Leave context.

        Arm the context sentry again.
        """
        self._ctx = None
        return False

    def __requirescontext(func: Callable) -> Callable:
        """Decorator to forbid usage out-of-context"""

        @wraps(func)
        def __wrapper(self, *pargs, **kwargs):
            try:
                assert self._ctx is not None
            except AssertionError as exc:
                raise OutOfContextError(textwrap.dedent(f'''
                    no context established for "{func.__name__}".  Did you use a with-statement?
                ''').strip()) from exc
            return func(self, *pargs, **kwargs)

        return __wrapper

    @__requirescontext
    def __str__(self) -> str:
        """Pretty printing."""
        return __class__.__doc__

    @__requirescontext
    def __call__(self):
        """Allow the runner to be called if the context sentry allows it."""
        pass

if __name__ == '__main__':
    """Self-test code"""

    import pytest

    with MweRunner() as R:
        R()
        print(repr(R))
        print(R)

    R = MweRunner()
    with pytest.raises(OutOfContextError):
        R()

    with pytest.raises(OutOfContextError):
        print(R)

    # This can be called outwith a context
    print(repr(R))
