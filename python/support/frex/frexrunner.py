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
        except AssertionError as exc:
            self._logger.log(logging.ERROR, 'No CPU info found')
            raise FileNotFoundError from exc
        try:
            assert self._sensors is not None
        except AssertionError from exc:
            self._logger.log(logging.ERROR, 'lm sensors package seems missing from system')
            raise FileNotFoundError from exc
        try:
            assert self._min_frex_file.exists()
        except AssertionError from exc:
            self._logger.log(logging.ERROR, 'Cannot find info regarding CPU minimum frequency')
            raise FileNotFoundError from exc

        self._logger.debug('Context established')
        return self

    def _det_min_frex(self) -> float:

        self._logger.debug('Determining min frex')
        with open(self._min_frex_file) as _min_frex:
            for i in _min_frex:
                _minimum_freq = i.rstrip() or 0
        # Make number and normalise to MHz
        _minimum_freq = int(_minimum_freq) / 1000
        self._logger.debug('Minimum frequency is {mf}'.format(mf=_minimum_freq))

        return _minimum_freq

    def _det_frex_gov(self, of_cpu) -> str:

        try:
            _scaling_gov_file = Path(
                '/sys/devices/system/cpu/cpu' + str(of_cpu)) / Path('cpufreq/scaling_governor')
            assert _scaling_gov_file.exists()
            with open(_scaling_gov_file) as _scaling_governor:
                return _scaling_governor.readlines()[0]
        except AssertionError:
            self._logger.log(logging.ERROR, _scaling_gov_file, 'does not exist')

    def _provide_overshoots(self, allowance, no_cpus):

        self._logger.debug('Find fast CPUs et al.')
        _how_many = 0
        print('CPUs running faster than', allowance, 'MHz:')
        with open(Path('/proc/cpuinfo')) as _cpuinfo:
            for _line in _cpuinfo.readlines():
                if 'processor' in _line:
                    _core = _line
                    _this_cpu = _core.split(':')[1].strip()
                if 'model name' in _line:
                    _model = _line
                if 'cpu MHz' in _line:
                    _mhz = float(_line.split(':')[1].lstrip())
                    if _mhz > allowance:
                        _how_many = _how_many + 1
                        _frex_gov = self._det_frex_gov(_this_cpu)
                        print(_core, _model, _line, 'frex governor   : ',_frex_gov, sep='', end='')

        print('That is,', _how_many, 'out of', no_cpus)

    def _provide_temp_readings(self):

        _temps = subprocess.check_output('sensors').decode().rstrip()

        for _line in _temps.splitlines():
            if 'CPU Temperature' in _line:
                print(_line)
            if 'MB Temperature' in _line:
                print(_line)

    def __call__(self):
        """Do the work."""
        super().__call__()

        self._logger.debug('Begining real work')

        _minimum_freq = self._det_min_frex()

        # 5 percent
        _margin = 1.05
        _allowance = _minimum_freq * _margin

        _no_cpus = subprocess.check_output('nproc').decode().rstrip()
        self._logger.debug('Found {n} CPUs'.format(n=_no_cpus))

        self._provide_overshoots(_allowance, _no_cpus)

        self._provide_temp_readings()

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
