"""Print the frequencies and related info of CPUs running faster than the minimum frequency.

This is followed by the temperature readings of the CPUs and the motherboard.  Depends on the
presence of a /proc filesystem, and the availability of the lm sensors tools.
"""
import argparse
from pathlib import Path
import textwrap
import shutil
import logging
import subprocess

from support.runmwe.mwerunner import MweRunner

class FrexRunner(MweRunner):

    def __init__(self, args):
        """Save passed-in info."""
        super().__init__()

        self._args = args
        self._CPU_Info = Path('/proc/cpuinfo');
        self._sensors = shutil.which('sensors')
        self._min_frex_file = Path('/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq')

        logging.basicConfig(level=logging.INFO)
        self._logger.debug('Init completed')

    def __enter__(self):
        """Establish context."""
        super().__enter__()

        try:
            assert self._CPU_Info.exists()
        except AssertionError:
            self._logger.log(logging.ERROR, 'No CPU info found')
            raise FileNotFoundError
        try:
            assert self._sensors is not None
        except AssertionError:
            self._logger.log(logging.ERROR, 'lm sensors package seems missing from system')
            raise FileNotFoundError
        try:
            assert self._min_frex_file.exists()
        except AssertionError:
            self._logger.log(logging.ERROR, 'Cannot find info regarding CPU minimum frequency')
            raise FileNotFoundError

        self._logger.debug('Context established')
        return self

    def __call__(self):
        """Do the work."""
        super().__call__()

        self._logger.debug('Begining real work')

        self._logger.debug('Determining min frex')
        with open(self._min_frex_file) as _min_frex:
            for i in _min_frex:
                _minimum_freq = i.rstrip() or 0
        # Make number and normalise to MHz
        _minimum_freq = int(_minimum_freq) / 1000
        self._logger.debug('Minimum frequency is {mf}'.format(mf=_minimum_freq))

        # 5 percent
        _margin = 1.05
        _allowance = _minimum_freq * _margin

        _no_cpus = subprocess.check_output('nproc').decode().rstrip()
        self._logger.debug('Found {n} CPUs'.format(n=_no_cpus))

        self._logger.debug('Done')

    def __exit__(self, exc_type, exc_value, traceback):
        """Seal the runner again when leaving the context."""
        super().__exit__(exc_type, exc_value, traceback)

        self._logger.debug('Context left')
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
