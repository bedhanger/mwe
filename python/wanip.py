#!/usr/bin/env python
"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
__all__ = [
    'naime',
]
import random
import sys
from support.wanip import (
    curlme,
    parse_cmd_line,
)
def naime():
    """
    Run the show
    """
    args = parse_cmd_line()
    provider, verbose = args.provider, args.verbose

    if provider:
        providers = [provider]
    else:
        providers = [
            'https://ifconfig.me/ip',
            'https://my.ip.fi',
            'https://icanhazip.com',
            'https://ifconfig.co',
            'https://ipecho.net/plain',
            'https://ipinfo.io/ip',
            'https://ident.me',
            'https://ip.tyk.nu/',
            'https://whatismyip.akamai.com',
            'https://eth0.me/',
            'https://api.ipify.org',
            'https://ip.me',
            'https://checkip.amazonaws.com',
            'https://ipgrab.io',
            'https://www.trackip.net/ip',
        ]
    provider = random.choice(providers)

    if verbose > 1: print(providers)
    if verbose >= 1: print('Trying {provider}'.format(provider=provider))

    curlme(provider=provider)

if __name__ == '__main__':
    sys.exit(naime())
