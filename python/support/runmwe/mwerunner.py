#!/usr/bin/env python
"""Base class for runners in MWE."""

class MweRunner:
    """A context-aware runner from which others may be instantiated from."""

    def __new__(cls, *pargs, **kwargs):
        """Make a runner."""
        return super().__new__(cls)

    def __init__(self):
        """Init a newly made runner."""

    def __enter__(self):
        """Establish context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Leave context."""
        return False

    def __call__(self):
        """Allow the runner to be called."""

    def __repr__(self):
        """Tell the world who we are, and where."""
        return str(type(self)) + ' @ ' + hex(id(self))
