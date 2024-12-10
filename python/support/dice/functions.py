import sys
import argparse
from termcolor import colored
import random

def parse_cmd_line(me: str, purpose: str):
    """
    Read options, show help
    """
    try:
        parser = argparse.ArgumentParser(
            prog=me,
            description=purpose,
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

def cast_die(whatever: object, eyes: int) -> None:
    """
    Roll it
    """
    if not whatever:
        whatever = range(1, eyes + 1)
    cast = random.choice(whatever)
    print(colored('{cast}', 'green', None, ['bold']).format(cast=cast))

def naime(me: str, purpose: str):
    """
    Run the show
    """
    # Parse the command line
    try:
        args = parse_cmd_line(me, purpose)
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
        cast_die(items, eyes)
    except:
        sys.stderr.write(colored("Die won't roll!\n", 'red'))
        raise
