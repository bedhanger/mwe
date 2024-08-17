#!/usr/bin/env python

PURPOSE = 'Ask a provider for your external wan ip with which you connect to it, then print it out'
HINT = 'Respect the netiquette when contacting the provider'
DEFAULT_PROVIDER = 'ifconfig.me/ip'

import argparse
import os
import subprocess
import sys

# Identify ourselves
ME = os.path.basename(__file__)

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
url = args.url
add_trailing_lf = args.add_trailing_newline

# Use curl to get the data
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
