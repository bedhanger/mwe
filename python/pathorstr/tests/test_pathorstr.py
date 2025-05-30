#!/usr/bin/env --split-string=python -m pytest --verbose

import pytest
from pathlib import Path
from typing import Union, TypeAliasType

from pathorstr import PathOrStr

def test_general():
    assert type(PathOrStr) is Union or TypeAliasType
