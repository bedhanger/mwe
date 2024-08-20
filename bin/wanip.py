#!/usr/bin/env python

__PURPOSE__ = 'Ask a provider for your ip with which you connect to it, then print it out'
__HINT__ = 'Respect the netiquette when contacting the provider'

__all__ = [
    'run_wanip',
]

def naime():

    def curlme(url, add_trailing_lf):
        """
        Use curl to get hold of my WANIP
        """
        import subprocess
        import sys

        # Construct curl command
        curl_cmd = f'curl --fail --show-error --silent {url}'

        # Obtain data & report
        result = subprocess.run(curl_cmd, shell=True, capture_output=True)
        if result.returncode != 0:
            sys.stderr.write(f'Cannot retrieve your WAN IP address from "{url}"\n')
            sys.stderr.write(f'The error message is this: {result.stderr.decode()}')
        else:
            sys.stdout.write(f'{result.stdout.decode()}')
            if add_trailing_lf:
                sys.stdout.write('\n')
        # Bye
        sys.exit(result.returncode)

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
            description=__PURPOSE__,
            epilog=__HINT__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            '-u', '--url',
            type=str,
            # This should simply return the address it sees in the connection
            default='https://ifconfig.me/ip',
            help='the URL to contact',
        )
        parser.add_argument(
            '-n', '--add-trailing-newline',
            action='store_true',
            default=False,
            help='add a trailing newline character to the output, purely cosmetic',
        )
        args = parser.parse_args()
        return (args.url, args.add_trailing_newline)

    url, add_trailing_lf = parse_cmd_line()
    curlme(url=url, add_trailing_lf=add_trailing_lf)

if __name__ == '__main__':
    naime()
