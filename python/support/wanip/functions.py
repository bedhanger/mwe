import subprocess
import sys
import argparse
import random
from .providers import public_providers

def curlme(provider):
    """
    Use curl to get hold of my WANIP
    """
    # Construct curl command
    curl_cmd = f'curl --fail --show-error --silent {provider}'

    # Obtain data & report
    result = subprocess.run(curl_cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        print(f'Cannot retrieve your WAN IP address from "{provider}"', file=sys.stderr)
        print(f'The error message is this: {result.stderr.decode()}', end='', file=sys.stderr)
    else:
        print('{output}'.format(output=result.stdout.decode().rstrip()))

def parse_cmd_line(me: str, purpose: str):
    """
    Read options, show help
    """
    # Parse the command line
    parser = argparse.ArgumentParser(
        prog=me,
        description=purpose,
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

def naime(me: str, purpose: str):
    """
    Run the show

    The LEGB scoping rule means that in order to overwrite the public_providers (a sensible thing to
    do in case the -p/--provider option has been specified), we must declare it as global.
    """
    global public_providers

    args = parse_cmd_line(me, purpose)
    provider, verbose = args.provider, args.verbose

    if provider:
        public_providers = [provider]
    provider = random.choice(public_providers)

    if verbose > 1: print(public_providers)
    if verbose >= 1: print('Trying {provider}'.format(provider=provider))

    curlme(provider=provider)
