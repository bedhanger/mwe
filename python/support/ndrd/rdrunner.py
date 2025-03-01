"""Remove the most recent temporary directory created by nd.py.

This works if executed in the same environment as the corresponding nd.py.
You should, like in the case of nd.py, eval this script.
"""
import os
import argparse
from termcolor import colored
import sys
from pathlib import Path
import textwrap

from support.runmwe.mwerunner import MweRunner

# Note that everything that is printed but that does *not* go to stderr is for the calling shell to
# eval.

class RDRunner(MweRunner):

    def __init__(self, args):
        """Save passed-in info."""
        super().__init__()

        self._args = args

    def __enter__(self):
        """If there's no ND, report that, and what can be done about it."""
        super().__enter__()

        try:
            self._nd = os.environ['ND']
            self._nd = Path(self._nd).resolve()
            assert self._nd.exists()
            return self
        except KeyError:
            print(colored(textwrap.dedent('''
                No temporary dir bound to env var ND, re-run with ND pointing to a folder.
            ''').lstrip(), 'red', None, None, force_color=True), end='', file=sys.stderr)
            raise NameError('No previous temporary folder')
        except AssertionError:
            print(colored(textwrap.dedent('''
                Though there is an ND, the corresponding folder does not exist.
                Suggest to unset the stale ND.
            ''').lstrip(), 'red', None, None, force_color=True), end='', file=sys.stderr)
            raise FileNotFoundError('Temporary folder gone?!?')

    def __call__(self):
        """Do the work."""
        super().__call__()

        _verbose = '--verbose' if self._args.verbose else ''

        # Shred every file, rename it several times, and finally remove it.  Remove the empty dir
        # skeleton afterwards.  Unset the ND variable.
        print(
            'cd',
            'find {ND} -type f -print0 | xargs --null --max-args=$(nproc) --no-run-if-empty \
                shred --force --remove {verbose} --exact --zero'.format(ND=self._nd, verbose=_verbose),
            'rm --recursive --force {verbose} {ND}'.format(ND=self._nd, verbose=_verbose),
            'unset ND',
            end='',
            sep=' && ',
        )

    def __exit__(self, exc_type, exc_value, traceback):
        """Seal the runner again when leaving the context."""
        super().__exit__(exc_type, exc_value, traceback)

        # Epilog
        print(colored(textwrap.dedent('''
            Good, that went well...
            Your shell has been tasked with shredding the folder.
        ''').lstrip(), 'green', None, ['bold'], force_color=True), end='', file=sys.stderr)

        return False

def parse_cmd_line(me):
    """Get options, show help """

    parser = argparse.ArgumentParser(
        prog=me,
        description=__doc__,
        epilog='Evaling means "eval $({me})"'.format(me=me),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show details of what is being done',
    )
    return parser.parse_args()
