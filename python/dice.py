#!/usr/bin/env python
"""
Play dice with the cmd line args.

When no args are given, simulate casting a die.
"""
import sys
from termcolor import colored
import subprocess
import argparse
import os
from random import choice

def naime():
    """
    Run the show
    """
    # Identify ourselves
    ME = os.path.basename(__file__)

    def parse_cmd_line():
        """
        Read options, show help
        """
        try:
            parser = argparse.ArgumentParser(
                prog=ME,
                description=__doc__,
                epilog=None,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            parser.add_argument(
                'items',
                nargs='*',
                help='the items to pseudo-randomly select from',
            )
            parser.add_argument(
                '-e', '--eyes',
                type=int,
                default='6',
                help='the number of eyes of the die',
            )
            return parser.parse_args()
        except argparse.ArgumentError:
            sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
            raise
    pass

    # Parse the command line
    try:
        args = parse_cmd_line()
        items = args.items
        eyes = args.eyes
    except SystemExit:
        # When the user requested help, the arg parser displays it and concludes with a sys.exit(0).
        # As this is an exception, we must handle it and finish the job.
        sys.exit(0)
    except:
        sys.stderr.write(colored('Cannot seem to begin; utterly confused & bailing out\n', 'red'))
        raise

    try:
        if not items:
            items = list(range(1, eyes + 1))
        print(colored('{cast}', 'green', None, ['bold']).format(cast=choice(items)))
    except subprocess.CalledProcessError as e:
        sys.stderr.write(colored('Cannot offload work to other commands!\n', 'red'))
        sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
        raise
    except:
        sys.stderr.write(colored('Oh!\n', 'red'))
        raise
pass

if __name__ == '__main__':
    try:
        naime()
    except Exception as e:
        sys.stderr.write(colored('Hm, that did not work: {what} ({hint})\n', 'red', None, ['bold']).
            format(what=e, hint=type(e)))
        sys.exit(-1)
