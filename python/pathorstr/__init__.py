"""
Define the type alias PathOrStr
"""
from sys import version_info
from typing import Union
from pathlib import Path

__all__ = ['PathOrStr']

if version_info < (3, 12):
    PathOrStr = Union[Path, str]
else:
    type PathOrStr = Union(Path, str)
