#!/usr/bin/env python
"""
Wrapper for the wanip script
"""
__all__ = [
    'naime',
]
import random
import sys
from support.wanip import (
    curlme,
    parse_cmd_line,
    providers,
)
def naime(providers):
    """
    Run the show
    """
    args = parse_cmd_line()
    provider, verbose = args.provider, args.verbose

    if provider:
        providers = [provider]
    provider = random.choice(providers)

    if verbose > 1: print(providers)
    if verbose >= 1: print('Trying {provider}'.format(provider=provider))

    curlme(provider=provider)

if __name__ == '__main__':
    sys.exit(naime(providers))
