#!/usr/bin/env python
"""
Utilise Youtube downloader.  Get the most recent Tagesschau by default.
"""
import sys
from pathlib import PurePath
from support.get_latest_tagesschau.functions import naime

if __name__ == '__main__':
    me = PurePath(__file__).name
    sys.exit(naime(me, __doc__))
