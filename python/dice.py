#!/usr/bin/env python
"""
Play dice with the cmd line args.

When no args are given, simulate casting a die.
"""
import sys
from termcolor import colored
import argparse
import os
import random

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
            items = range(1, eyes + 1)
        print(colored('{cast}', 'green', None, ['bold']).format(cast=random.choice(items)))
    except OverflowError:
        sys.stderr.write(colored('Cannot construct such a huge die!\n', 'red'))
        raise
    except:
        sys.stderr.write(colored('Oh!\n', 'red'))
        raise
pass

if __name__ == '__main__':
    try:
        naime()
    except Exception as exc:
        sys.stderr.write(colored('Hm, that did not work: {what} ({hint})\n', 'red', None, ['bold']).
            format(what=exc, hint=type(exc)))
        sys.exit(-1)
