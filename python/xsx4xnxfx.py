#!/usr/bin/env python

"""
Try to use 'x' a lot
"""

from support.selfpylint.linter import run_selfpylint

# Original list
x = []
x = [0, True, 1, 'x', False, 7, 8, None, x]
print(x)

# Now filter out the ones that ain't
x = [x for x in x if x]
print(x)

run_selfpylint(__file__)
