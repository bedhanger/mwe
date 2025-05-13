#!/usr/bin/env python
"""Base class for runners in MWE."""

import logging

from support.lsattr import LsAttr

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

    def __str__(self) -> str:
        """Pretty printing."""
        return __class__.__doc__

    def __call__(self):
        """Allow the runner to be called if the context sentry allows it."""
        assert self._ctx is not None, 'No context established.  Did you use a with-statement?'

if __name__ == '__main__':
    print(repr(MweRunner()))
