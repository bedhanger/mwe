"""
Ask a provider for your ip with which you connect to it, then print it out.
"""
import subprocess
import sys
import pathlib
import argparse

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

def parse_cmd_line():
    """
    Read options, show help
    """
    # Identify ourselves
    ME = pathlib.PurePath(__file__).stem

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
