"""
Define PathOrStr as a type alias or at least as a union
"""
from sys import version_info
from pathlib import Path

__all__ = ['PathOrStr']

PathOrStr = Path | str
if version_info >= (3, 12):
    type PathOrStr = PathOrStr
