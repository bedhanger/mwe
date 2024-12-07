#!/usr/bin/env python
"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
__all__ = [
    'naime',
]
import random
import sys
import subprocess
import argparse
import os

def naime():
    """
    Run the show
    """
    def curlme(provider):
        """
        Use curl to get hold of my WANIP
        """
        # Construct curl command
        curl_cmd = f'curl --fail --show-error --silent {provider}'

        # Obtain data & report
        result = subprocess.run(curl_cmd, shell=True, capture_output=True)
        if result.returncode != 0:
            sys.stderr.write(f'Cannot retrieve your WAN IP address from "{provider}"\n')
            sys.stderr.write(f'The error message is this: {result.stderr.decode()}')
        else:
            print('{output}'.format(output=result.stdout.decode().rstrip()))

    def parse_cmd_line():
        """
        Read options, show help
        """
        # Identify ourselves
        ME = os.path.basename(__file__)

        # Parse the command line
        parser = argparse.ArgumentParser(
            prog=ME,
            description=__doc__,
            epilog='Respect the netiquette when contacting the provider.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            '-p', '--provider',
            type=str,
            help='''
                the provider to contact, instead of pseudo-randomly auto-selecting one from a
                pre-built internal list
                ''',
        )
        parser.add_argument(
            '-v', '--verbose',
            action='count',
            default=0,
            help='''
                used once: show which provider will be contacted; used twice (or more often):
                display contactable providers as well (i.e., the pre-built internal list)
                ''',
        )
        return parser.parse_args()

    # Go
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
