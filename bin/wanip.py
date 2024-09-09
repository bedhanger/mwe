#!/usr/bin/env python
"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
__all__ = [
    'naime',
]
import random

def naime():

    def curlme(provider, add_trailing_lf):
        """
        Use curl to get hold of my WANIP
        """
        import subprocess
        import sys

        # Construct curl command
        curl_cmd = f'curl --fail --show-error --silent {provider}'

        # Obtain data & report
        result = subprocess.run(curl_cmd, shell=True, capture_output=True)
        if result.returncode != 0:
            sys.stderr.write(f'Cannot retrieve your WAN IP address from "{provider}"\n')
            sys.stderr.write(f'The error message is this: {result.stderr.decode()}')
        else:
            sys.stdout.write(f'{result.stdout.decode()}')
            if add_trailing_lf:
                sys.stdout.write('\n')
        # Bye
        sys.exit(result.returncode)
    pass

    def parse_cmd_line():
        """
        Read options, show help
        """
        import argparse
        import os

        # Identify ourselves
        ME = os.path.basename(__file__)

        # Parse the command line
        parser = argparse.ArgumentParser(
            prog=ME,
            description=__doc__,
            epilog='Respect the netiquette when contacting the provider.',
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            '-p', '--provider',
            type=str,
            help='the provider to contact, instead of pseudo-randomly auto-selecting one',
        )
        parser.add_argument(
            '-n', '--add-trailing-newline',
            action='store_true',
            help='add a trailing newline character to the output, purely cosmetic',
        )
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='show which provider will be contacted',
        )
        return parser.parse_args()
    pass

    # Go
    args = parse_cmd_line()
    provider, add_trailing_lf, verbose = args.provider, args.add_trailing_newline, args.verbose

    if not provider:
        providers = [
            'https://ifconfig.me/ip',
            'https://my.ip.fi',
            'https://icanhazip.com',
            'https://ifconfig.co',
            'https://ipecho.net/plain',
            'https://ipinfo.io/ip',
            'https://ident.me',
        ]
        provider = random.choice(providers)

    if verbose:
        print('Trying {provider}'.format(provider=provider))

    curlme(provider=provider, add_trailing_lf=add_trailing_lf)
pass

if __name__ == '__main__':
    naime()
