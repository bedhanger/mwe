#!/usr/bin/env python

"""Run the runner for rd."""

from pathlib import PurePath

from support.ndrd.rdrunner import RDRunner, parse_cmd_line

if __name__ == '__main__':

    me = PurePath(__file__).name
    args = parse_cmd_line(me)

    with RDRunner(args) as rdr:
        rdr()
