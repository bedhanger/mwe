"""Base class for runners in MWE."""

import logging
from typing import Callable, Self
from functools import wraps
import textwrap

from lsattr import LsAttr
from ooce.exceptions import OutOfContextError

class MweRunner(LsAttr):
    """A context-aware runner others may be instantiated from"""

    @classmethod
    def __new__(cls, *pargs, **kwargs):
        """Make a runner."""
        return object.__new__(cls)

    def __init__(self):
        """Init a newly made runner."""
        # Simplistic form of protection against not instigating the context manager protocol
        self._ctx = None
        self._logger = None

    def __enter__(self) -> Self:
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
                raise OutOfContextError(cls=self.__class__.__name__, func=func.__name__) from exc
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
