#!/usr/bin/env python

"""Run the runner for nd."""

from pathlib import PurePath

from support.ndrd.ndrunner import NDRunner, parse_cmd_line

if __name__ == '__main__':

    me = PurePath(__file__).name
    args = parse_cmd_line(me)

    with NDRunner(args) as ndr:
        ndr()
