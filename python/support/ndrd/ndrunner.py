"""Create a new temporary directory and jump into it.

For the latter to work, you should eval this script, rather than execute it directly.
"""
import argparse
from termcolor import colored
import subprocess
import random
import os
import sys
from pathlib import Path
import textwrap

from support.runmwe.mwerunner import MweRunner

# Note that everything that is printed but that does *not* go to stderr is for the calling shell to
# eval.

class NDRunner(MweRunner):

    def __init__(self, args):
        """Save passed-in info."""
        super().__init__()
        self._args = args

    def __enter__(self):
        """Bail out if the env says we already have an ND.

        Returning None (raising an exception) makes a subsequent call impossible.
        """
        try:
            self._nd = os.environ['ND']
            raise RecursionError('Attempt to nest operations: ND already is', self._nd)
        except KeyError:
            super().__enter__()
            # We are good to go
            return self

    def __call__(self):
        """Do the work."""
        super().__call__()

        # Construct the name of the directory.  The calls to the replace methods afterwards are
        # concessions to one of the many shortcomings of NTFS in Win32 namespace, namely, the
        # boggling list (both in terms of length and content) of which characters are *not* allowed
        # in filenames.
        tmp_name = [
            # It should be readable, which is why UUIDs are not suitable; or tempfile, for that
            # matter.
            'date --iso-8601=seconds',
        ]
        tmp_name = subprocess.run(tmp_name, shell=True, check=True, capture_output=True)
        self._nd = tmp_name.stdout.decode().strip()

        self._nd = self._nd.replace(':', '-')
        self._nd = self._nd.replace('+', 'plus')
        self._nd = self._nd + '-' + str(os.getpid()) + '-' + str(random.randrange(32768))

        # Where to create it.  Obey user's choice: first arg, then env var, and finally /tmp, in
        # that order.  As a last-ditch effort, fall back to the cwd.
        where = self._args.tmp_root
        try:
            assert where is not None
        except AssertionError:
            try:
                where = os.environ['ND_ROOT']
            except KeyError:
                where = '/tmp'
        finally:
            try:
                assert where is not None
            except AssertionError:
                where = '.'

        # Now build a proper path
        self._nd = (Path(where) / Path(self._nd)).resolve()

        # Now make a folder
        try:
            self._nd.mkdir(parents=True)
        except FileExistsError:
            raise FileExistsError("Name collision?!?")
        else:
            print(colored('Made a folder in {nd}', 'green', None, None, force_color=True).format(
                nd=self._nd), file=sys.stderr)

    def __exit__(self, exc_type, exc_value, traceback):
        """Seal the runner again when leaving the context."""
        super().__exit__(exc_type, exc_value, traceback)

        # Print commands for the shell
        print(
            'export ND={nd}'.format(nd=self._nd),
            'cd ${ND}',
            'stat .',
            end='',
            sep=' && ',
        )

        # This is not for the shell...
        print(colored(textwrap.dedent('''
            Good, that went well...
            Your shell has been tasked with making the new folder known, getting you there,
            and showing some general info about it.
        ''').lstrip(), 'green', None, ['bold'], force_color=True), end='', file=sys.stderr)

        return False

def parse_cmd_line(me):
    """Get options, show help."""
    parser = argparse.ArgumentParser(
        prog=me,
        description=__doc__,
        epilog='Evaling means "eval $({me})"'.format(me=me),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'tmp_root',
        nargs='?',
        help='parent folder of the temp folder',
    )
    return parser.parse_args()
