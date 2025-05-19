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
    """A context-aware runner others may be instantiated from"""

    def __new__(cls, *pargs, **kwargs):
        """Make a runner."""
        return object.__new__(cls)

    def __init__(self):
        """Init a newly made runner."""
        # Simplistic form of protection against not instigating the context manager protocol
        self._ctx = None
        self._logger = None

    def __enter__(self):
        """Establish context.

        Appease the context sentry, and set up the logger..
        """
        self._ctx = hex(id(self))
        self._logger = logging.getLogger()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Leave context.

        Arm the context sentry again, and relinquish the logger.
        """
        self._ctx = None
        self._logger = None
        return False

    def __requirescontext(func: Callable) -> Callable:
        """Decorator to forbid usage out-of-context"""

        @wraps(func)
        def __wrapper(self, *pargs, **kwargs):
            try:
                assert self._ctx is not None
            except AssertionError as exc:
                raise OutOfContextError(textwrap.dedent(f'''
                    no context has been established before invoking {func.__name__!r}

                    Did you forget to use a with-statement?

                    {self.__class__.__name__!r} requires that the context-manager-protocol be used
                    when instances of it are created.  This was a conscious design decision, aimed
                    at facilitating resource management (freeing the resource, in particular).  So
                    rather than saying something like

                    >>> R = {self.__class__.__name__}()
                    >>> print(R)

                    do this instead

                    >>> with {self.__class__.__name__}() as R:
                    >>>     print(R)

                    Outwith a context, R is practically unusable.
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
        import this

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
