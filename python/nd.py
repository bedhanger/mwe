#!/usr/bin/env python
"""Create a new temporary directory and jump into it.

For the latter to work, you should eval this script, rather than execute it directly.
"""
from pathlib import PurePath

from support.ndrd.ndrunner import NDRunner, parse_cmd_line

if __name__ == '__main__':

    me = PurePath(__file__).name
    args = parse_cmd_line(me)

    with NDRunner(args) as ndr:
        ndr()
