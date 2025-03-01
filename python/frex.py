#!/usr/bin/env python

"""Run the runner for frex."""

from pathlib import PurePath

from support.frex.frexrunner import FrexRunner, parse_cmd_line

if __name__ == '__main__':

    me = PurePath(__file__).name
    args = parse_cmd_line(me)

    with FrexRunner(args) as frxr:
        frxr()
