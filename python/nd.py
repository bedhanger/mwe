#!/usr/bin/env python

"""
Create a new temporary directory and jump into it.  For the latter to work, you should eval this
script, rather than execute it directly.
"""

import sys
from termcolor import colored
import subprocess
import argparse
import os
import random
from pathlib import Path

# Note that everything that is printed but that does *not* go to stderr is for the calling shell to
# eval.

class ExistingNDError(Exception): pass
class NoNDSituation(Exception): pass # The good case, actually...

def parse_cmd_line():
    """
    Get options, show help
    """
    me = os.path.basename(__file__)
    try:
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
    except argparse.ArgumentError:
        sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
        raise

def handle_existing_nd():
    """
    React to previous "incarnations" of this
    """
    try:
        nd = os.environ['ND']
        print(colored('''\
No, you don\'t wanna nest this stuff.  ND currently is "{nd}"
This may be due to a wedged previous "state".  Use that or unset it & try again
''', 'red', None, None).format(nd=nd), end='', file=sys.stderr)
        raise ExistingNDError('Attempt to nest operations')
    except KeyError:
        # All good, transfer to the pure state
        raise NoNDSituation

def handle_new_nd():
    """
    Go
    """
    # Construct the name of the directory.  The calls to the replace methods afterwards are
    # concessions to one of the many shortcomings of NTFS in Win32 namespace, namely, the
    # boggling list (both in terms of length and content) of which characters are *not* allowed
    # in filenames.
    try:
        tmp_name = [
            # It should be readable, which is why UUIDs are not suitable...
            'date --iso-8601=seconds',
        ]
        tmp_name = subprocess.run(tmp_name, shell=True, check=True, capture_output=True)
        nd = tmp_name.stdout.decode().strip()

        nd = nd.replace(':', '-')
        nd = nd.replace('+', 'plus')
        nd = nd + '-' + str(os.getpid()) + '-' + str(random.randrange(32768))
    except subprocess.CalledProcessError as exc:
        print(colored('{what} ({hint})', 'red', None, None).format(what=exc,
                                                                   hint=type(exc)),
              file=sys.stderr)
        raise
    except:
        raise

    # Where to create it.  Obey user's choice: first arg, then env var, and finally /tmp, in that
    # order.  As a last-ditch effort, fall back to the cwd.
    try:
        arg = parse_cmd_line()
        where = arg.tmp_root
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
    nd = (Path(where) / Path(nd)).resolve()

    # Now make a folder
    try:
        nd.mkdir(parents=True)
    except FileExistsError:
        raise FileExistsError("Name collision?!?")
    else:
        print(colored('Made a folder in {nd}', 'green', None, None).format(nd=nd), file=sys.stderr)

    print(
        'export ND={nd}'.format(nd=nd),
        'cd ${ND}',
        'stat .',
        end='',
        sep=' && ',
    )

def naime():
    """
    Run the show
    """
    try:
        handle_existing_nd()
    except NoNDSituation:
        handle_new_nd()
    except:
        raise

if __name__ == '__main__':
    try:
        naime()
    except Exception as exc:
        print(colored('Hm, that did not work: {what} ({hint})', 'red', None, ['bold']).
            format(what=exc, hint=type(exc)), file=sys.stderr)
        sys.exit(-1)
    else:
        print(colored('''\
Good, that went well...
Your shell has been tasked with making the new folder known, getting you there,
and showing some general info about it.
''', 'green', None, ['bold']), end='', file=sys.stderr)
