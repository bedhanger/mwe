#!/usr/bin/env python

"""
Remove the most recent temporary directory created by nd.py, if executed in the same environment as
the corresponding nd.py.
You should, like in the case of nd.py, eval this script.
"""

import sys
try:
    from termcolor import colored
except ModuleNotFoundError:
    def colored(_, *pargs, **kwargs):
        return _
import subprocess
import argparse
import os
import random
from pathlib import Path, PurePath

# Note that everything that is printed but that does *not* go to stderr is for the calling shell to
# eval.

def parse_cmd_line():
    """
    Get options, show help
    """
    me = PurePath(__file__).name
    try:
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
    except argparse.ArgumentError:
        sys.stderr.write(colored('Could not decipher the command line\n', 'red', force_color=True))
        raise

def handle_existing_nd(verbose):
    """
    Get rid of the previously created ND
    """
    verbose = '--verbose' if verbose else ''
    try:
        nd = os.environ['ND']
        nd = Path(nd).resolve()

        # Shred every file, rename it several times, and finally remove it.  Remove the empty dir
        # skeleton afterwards.  Unset the ND variable.
        print(
            'cd',
            'find {ND} -type f -print0 | xargs --null --max-args=$(nproc) --no-run-if-empty \
                shred --force --remove {verbose} --exact --zero'.format(ND=nd, verbose=verbose),
            'rm --recursive --force {verbose} {ND}'.format(ND=nd, verbose=verbose),
            'unset ND',
            end='',
            sep=' && ',
        )
    except KeyError:
        raise NameError('No env var ND')

def handle_no_nd():
    """
    Report that there is nothing to do, and what can be done about it
    """
    print(colored('''\
No temporary dir bound to env var ND, re-run with ND pointing to a folder.
''', 'red', None, None, force_color=True), end='', file=sys.stderr)
    raise NameError('No previous temporary folder')

def naime():
    """
    Run the show
    """
    args = parse_cmd_line()
    verbose = args.verbose
    try:
        handle_existing_nd(verbose=True)
    except NameError:
        handle_no_nd()
    except:
        raise

if __name__ == '__main__':
    try:
        naime()
    except Exception as exc:
        print(colored('Hm, that did not work: {what} ({hint})', 'red', None, ['bold'], force_color=True).
            format(what=exc, hint=type(exc)), file=sys.stderr)
        sys.exit(-1)
    else:
        print(colored('''\
Good, that went well...
Your shell has been tasked with shredding the folder.
''', 'green', None, ['bold'], force_color=True), end='', file=sys.stderr)
