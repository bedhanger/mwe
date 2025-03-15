#!/usr/bin/env python
"""
TODO: write me
"""

from support.runmwe.mwerunner import MweRunner

class WanipzRunner(MweRunner):
    """Runner for wanipz."""

    def __init__(self):
        """Init the newly made runner."""
        super().__init__()

    def __enter__(self):
        """Build context and return it."""
        super().__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Leave context."""
        super().__exit__(exc_type, exc_value, traceback)
        return False

    def __call__(self):
        """Do the work."""
        super().__call__()
