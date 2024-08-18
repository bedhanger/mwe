#!/usr/bin/env python

PURPOSE = 'Ask a provider for your external wan ip with which you connect to it, then print it out'
HINT = 'Respect the netiquette when contacting the provider'

def run_wanip():

    def curlme(url, add_trailing_lf):
        """
        Use curl to get hold of my WANIP
        """
        import subprocess
        import sys

        # Construct curl command
        curl_cmd = f'curl --fail --show-error --silent {url}'

        # Obtain data & report
        result = subprocess.run(curl_cmd, shell = True, capture_output = True)
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

        # This should simply return the address it sees in the connection
        DEFAULT_PROVIDER = 'ifconfig.me/ip'

        # Parse the command line
        parser = argparse.ArgumentParser(
            prog = ME,
            description = PURPOSE,
            epilog = HINT,
        )
        parser.add_argument(
            '-u', '--url',
            type = str,
            default = DEFAULT_PROVIDER,
            help = f'the URL to contact; defaults to "{DEFAULT_PROVIDER}"',
        )
        parser.add_argument(
            '-n', '--add-trailing-newline',
            action = 'store_true',
            help = 'add a trailing newline character to the output, purely cosmetic',
        )
        args = parser.parse_args()
        return (args.url, args.add_trailing_newline)

    url, add_trailing_lf = parse_cmd_line()
    curlme(url, add_trailing_lf)

if __name__ == '__main__':
    run_wanip()
