"""Here be dragons"""

import subprocess
import sys
import argparse
from pathlib import PurePath
from typing import Optional

class Ncrvi:

    def __init__(self,
                 me: Optional[str] = PurePath(__file__).stem,
                 purpose : Optional[str] = __doc__) -> None:
        """Kick off scanning the command-line"""
        self.args = self.parse_cmd_line(me, purpose)

    def parse_cmd_line(self, me: str, purpose: str) -> Optional[argparse.Namespace]:
        """Read options, show help"""
        # Parse the command line
        try:
            parser = argparse.ArgumentParser(
                prog=me,
                description=purpose,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            parser.add_argument(
                '-w', '--initial-wait',
                default=0,
                help='''
                    number of seconds to wait before starting the tests
                    ''',
            )
            return parser.parse_args()
        except argparse.ArgumentError as exc:
            raise ValueError('The command-line is indecipherable')

    def __call__(self) -> None:
        """Run the show"""

        try:
            assert True is not False
        except AssertionError as exc:
            raise RuntimeError('You are in trouble') from exc

def __main():

    N = Ncrvi()
    N()

def main():
    try:
        __main()
    except Exception:
        import traceback
        print(traceback.format_exc(), file=sys.stderr, end='')
        sys.exit(1)
    except KeyboardInterrupt:
        print('Interrupted by user', file=sys.stderr, end='')
        sys.exit(1)

if __name__ == '__main__':
    main()
