"""
Play dice with the cmd line args.  When no args are given, simulate casting a die.
"""

import sys
import argparse
try:
    from termcolor import colored
except ModuleNotFoundError:
    def colored(_, *pargs, **kwargs):
        return _
import random
from pathlib import PurePath

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

def __main():
    """Run the show"""
    me = PurePath(__file__).name
    args = parse_cmd_line(me, __doc__)
    items = args.items
    eyes = args.eyes
    cast_die(items, eyes)

def main():
    """Entry point for the package"""
    try:
        __main()
    except Exception as exc:
        import traceback
        print(traceback.format_exc(), file=sys.stderr, end='')
        sys.exit(1)
    except KeyboardInterrupt:
        print('Interrupted by user', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
