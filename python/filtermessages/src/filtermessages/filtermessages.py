"""Omit from files/stdin empty and uninteresting lines"""

import sys
import re
import fileinput
import argparse

from pathlib import PurePath
from typing import Optional

class FilterMessages:

    DEFAULT_THINGS_CONSIDERED_BORING : re.Pattern = re.compile(r'''
        (?:b(ed)?h(anger)?\svdr:)
        |
        (?:(dovecot)|(log)(\[\d+\])?:\simap)
        |
        (?:b(ed)?h(anger)?\sfirefox(\.desktop)?(\[\d+\])?:)
        |
        (?:b(ed)?h(anger)?\smp3fs(\[\d+\])?:)
        |
        (?:b(ed)?h(anger)?\scron.*:)
        |
        (?:failed\sto\scoldplug\sunifying.*:)
        |
        (?:b(ed)?h(anger)?\ssmartd.*:.*SMART\sUsage\sAttribute:\s194\sTemperature_Celsius\schanged\sfrom)
        |
        (?:EMITTING\sCHANGED\sfor)
        |
        (?:helper\(pid\s+\d+\):\scompleted\swith\sexit\scode\s0)
        |
        (?:helper\(pid\s+\d+\):\slaunched\sjob\sudisks-helper-ata-smart-collect\son)
        |
        (?:Refreshing\sATA\sSMART\sdata\sfor)
        |
        (?:dvb_frontend_get_frequency_limits)
        |
        (?:systemd\[1\]:\sCondition\scheck\sresulted\sin\s.+\sbeing\sskipped\.)
        |
        (?:gdm-x-session\[\d+\]:\s>\sWarning:\s+Could\snot\sresolve\skeysym\s\S+)
    ''', re.VERBOSE)

    def __init__(self,
                 me: Optional[str] = PurePath(__file__).stem,
                 purpose : Optional[str] = __doc__
    ) -> None:
        """"Init the show"""
        self.args = self.parse_cmd_line(me, purpose)
        self.files = tuple(file for file in self.args.file) if self.args.file else None
        self.boring_regex = re.compile(self.args.boring_regex, re.VERBOSE)


    def parse_cmd_line(self, me: str, purpose: str) -> Optional[argparse.Namespace]:
        """Read options, show help"""
        try:
            parser = argparse.ArgumentParser(
                prog=me,
                description=purpose,
            )
            parser.add_argument(
                'file',
                nargs='*',
                default=None,
                help='''
                    work on this; use '-' to denote stdin
                    ''',
            )
            parser.add_argument(
                '-b', '--boring-regex',
                default=self.DEFAULT_THINGS_CONSIDERED_BORING.pattern,
                help='''
                    what to omit; the default is so complex, it cannot be printed here :-|
                    ''',
            )
            return parser.parse_args()
        except argparse.ArgumentError as exc:
            raise ValueError('The command-line is indecipherable')


    def __call__(self) -> int:
        """Run the show"""

        with fileinput.input(files=self.files) as file:

            for line in file:

                # Blank and blank-looking lines we discard
                if not line.strip():
                    continue

                # Ignore lines containing items explicitly declared uninteresting
                if self.boring_regex.search(line):
                    continue

                # This, by definition, is interesting
                print(line, end='')

        # All good
        return 0


def __main() -> int:

    Fm = FilterMessages()
    sys.exit(Fm())


def main() -> int:
    """TOML entry point for the script"""
    try:
        sys.exit(__main())
    except Exception:
        import traceback
        print(traceback.format_exc(), file=sys.stderr, end='')
        sys.exit(2)
    except KeyboardInterrupt:
        print('\rInterrupted by user', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    sys.exit(main())
