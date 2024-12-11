#!/usr/bin/env python
"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
import sys
from pathlib import PurePath
from support.wanip.functions import naime

# Identify ourselves
me = PurePath(__file__).name

if __name__ == '__main__':
    sys.exit(naime(me, __doc__))
