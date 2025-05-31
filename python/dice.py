#!/usr/bin/env python
"""
Play dice with the cmd line args.  When no args are given, simulate casting a die.
"""
import sys
from pathlib import PurePath
from dice import naime

if __name__ == '__main__':
    # Identify ourselves
    me = PurePath(__file__).name
    sys.exit(naime(me, __doc__))
