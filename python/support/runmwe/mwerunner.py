#!/usr/bin/env python
"""Base class for runners in MWE."""

class MweRunner:
    """A runner from which others may be instantiated from."""

    def __new__(cls, *pargs, **kwargs):
        """Make a runner."""
        return super().__new__(cls)

    def __init__(self):
        """Init a newly made runner."""

    def __call__(self):
        """Allow the runner to be called."""

    def __repr__(self):
        """Tell the world who we are, and where."""
        return str(type(self)) + ' @ ' + hex(id(self))
