#!/usr/bin/env python

"""Print sanity-check information of your WAN IP/registered domain."""

from pathlib import PurePath
import argparse
import sys
import logging
import subprocess
try:
    from termcolor import colored
except ModuleNotFoundError:
    def colored(_, *pargs, **kwargs):
        return _

from support.runmwe import MweRunner

class WanipzRunner(MweRunner):
    """Runner for wanipz."""

    def __init__(self):
        """Init the newly made runner."""
        super().__init__()

        logging.basicConfig(level=logging.INFO)

        self._ME = PurePath(__file__).name
        self._args = self._parse_cmd_line()

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

        self._display_cut_here()
        self._show_local_dns_info()
        self._display_cut_here()
        self._determine_wanip()
        self._display_cut_here()

    def _parse_cmd_line(self):
        """Read options, show help."""
        try:
            _parser = argparse.ArgumentParser(
                prog=self._ME,
                description=__doc__,
                epilog='Respect the netiquette when contacting external providers.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            return _parser.parse_args()
        except argparse.ArgumentError:
            self._logger.log(logging.ERROR, colored('Could not decipher the command line'), 'red')

    def _display_cut_here(self):
        """Show a distinctive visual divide."""
        scissors = '--->8' * 20
        self._logger.info(colored(scissors, 'yellow', None, None))

    def _show_local_dns_info(self):
        """"""
        try:
            self._logger.info(colored('What the local DNS server thinks; you must track an entry named "wanip" for this to work', 'blue', None, ['bold']))
            external_cmd = 'host -v wanip'
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            self._logger.info(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
        except subprocess.CalledProcessError as e:
            self._logger.log(logging.ERROR, colored('Cannot obtain info regarding "wanip" DNS record!', 'red'))
            self._logger.log(logging.ERROR, colored('{because}', 'red').format(because=e.stderr.decode()))

    def _determine_wanip(self):
        """"""
        try:
            self._logger.info(colored('Trying to determine your WANIP', 'blue', None, ['bold']))
            external_cmd = 'wanip --verbose'
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            print(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
            *_, _wan_ip = result.stdout.decode().split()
        except subprocess.CalledProcessError as e:
            self._logger.log(logging.ERROR, colored('Cannot obtain info regarding external IP address', 'red'))
            self._logger.log(logging.ERROR, colored('{because}', 'red').format(because=e.stderr.decode()))

        try:
            external_cmd = 'host -v {ptr_record}'.format(ptr_record=_wan_ip)
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            self._logger.info(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
        except subprocess.CalledProcessError as e:
            self._logger.log(logging.ERROR, colored('Cannot obtain reverse info regarding external IP address!', 'red'))
            self._logger.log(logging.ERROR, colored('{because}', 'red').format(because=e.stderr.decode()))
