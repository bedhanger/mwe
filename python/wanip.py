#!/usr/bin/env python
"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
import sys
from pathlib import PurePath
from support.wanip import naime

if __name__ == '__main__':
    # Identify ourselves
    me = PurePath(__file__).name
    sys.exit(naime(me, __doc__))
