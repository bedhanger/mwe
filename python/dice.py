#!/usr/bin/env python
"""
Play dice with the cmd line args.  When no args are given, simulate casting a die.
"""
import sys
from pathlib import PurePath
from support.dice.functions import naime

# Identify ourselves
me = PurePath(__file__).name

if __name__ == '__main__':
    sys.exit(naime(me, __doc__))
