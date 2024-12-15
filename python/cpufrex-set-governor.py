#!/usr/bin/env python
"""
Set the CPU frequency governing policy.
"""
import sys
from pathlib import PurePath
from support.cpufrex_set_governor.functions import naime

if __name__ == '__main__':
    # Identify ourselves
    me = PurePath(__file__).name
    sys.exit(naime(me, __doc__))
