"""Print the frequencies and related info of CPUs running faster than the minimum frequency.

This is followed by the temperature readings of the CPUs and the motherboard.  Depends on the
presence of a /proc filesystem, and the availability of the lm sensors tools.
"""
import argparse
from pathlib import Path
import textwrap

from support.runmwe.mwerunner import MweRunner

class FrexRunner(MweRunner):

    def __init__(self, args):
        """Save passed-in info."""
        super().__init__()

        self._args = args
        self._CPU_Info = Path('/proc/cpuinfo');

    def __enter__(self):
        """Establish context."""
        super().__enter__()

        try:
            assert self._CPU_Info.exists()
            return self
        except AssertionError:
            raise FileNotFoundError('No CPU info found')

    def __call__(self):
        """Do the work."""
        super().__call__()

    def __exit__(self, exc_type, exc_value, traceback):
        """Seal the runner again when leaving the context."""
        super().__exit__(exc_type, exc_value, traceback)

        return False

def parse_cmd_line(me):
    """Get options, show help."""

    parser = argparse.ArgumentParser(
        prog=me,
        description=__doc__,
        epilog=None,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    return parser.parse_args()
