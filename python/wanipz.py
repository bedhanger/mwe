#!/usr/bin/env python
"""
Print sanity-check information of your WAN IP/registered domain.
"""
import sys
from termcolor import colored
import subprocess
import argparse
import os
from socket import gethostbyname_ex, gethostname

def naime():
    """
    Run the show
    """
    # Identify ourselves
    ME = os.path.basename(__file__)

    def parse_cmd_line():
        """
        Read options, show help
        """
        try:
            parser = argparse.ArgumentParser(
                prog=ME,
                description=__doc__,
                epilog='Respect the netiquette when contacting external providers.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            return parser.parse_args()
        except argparse.ArgumentError:
            sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
            raise
    pass

    def wanipz():
        """
        Collect the info and show it
        """
        display_cut_here()

        try:
            print(colored('What the local DNS server thinks; you must track an entry named "wanip" for this to work', 'blue', None, ['bold']))
            external_cmd = 'host wanip'
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            print(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
        except subprocess.CalledProcessError as e:
            sys.stderr.write(colored('Cannot obtain info regarding "wanip" DNS record!\n', 'red'))
            sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
            raise
        except:
            sys.stderr.write(colored('Oh!\n', 'red'))
            raise

        display_cut_here()

        try:
            print(colored('Trying to determine your WANIP', 'blue', None, ['bold']))
            external_cmd = 'wanip'
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            print(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
            wan_ip = output=result.stdout.decode()
        except subprocess.CalledProcessError as e:
            sys.stderr.write(colored('Cannot obtain info regarding external IP address!\n', 'red'))
            sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
            raise
        except:
            sys.stderr.write(colored('Oh!\n', 'red'))
            raise

        try:
            external_cmd = 'host {ptr_record}'.format(ptr_record=wan_ip)
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            print(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
        except subprocess.CalledProcessError as e:
            sys.stderr.write(colored('Cannot obtain reverse info regarding external IP address!\n', 'red'))
            sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
            raise
        except:
            sys.stderr.write(colored('Oh!\n', 'red'))
            raise

        display_cut_here()

        try:
            # We're only interested in the first element of the tuple
            #     (canonical_hostname, list_of_alias_hostnames, list_of_IP_addresses)
            fqdn = gethostbyname_ex(gethostname())[0]

            # Cloudflare, try 'dns.google.' for Google
            public_dns = 'one.one.one.one.'

            print(colored('What a public DNS provider thinks about "{this_host}"',
                          'blue', None, ['bold']).format(this_host=fqdn))

            external_cmd = 'host {host} {ns}'.format(host=fqdn, ns=public_dns)
            result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
            print(colored('{output}', 'green').format(output=result.stdout.decode().strip()))
        except subprocess.CalledProcessError as e:
            sys.stderr.write(colored('Cannot query public DNS provider!\n', 'red'))
            sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
            raise
        except:
            sys.stderr.write(colored('Oh!\n', 'red'))
            raise

        display_cut_here()
    pass

    def display_cut_here():
        """
        Show a distinctive visual divide
        """
        scissors = '--->8' * 20
        print(colored(scissors, 'yellow', None, None))
    pass

    # Parse the command line
    try:
        args = parse_cmd_line()
    except SystemExit:
        # When the user requested help, the arg parser displays it and concludes with a sys.exit(0).
        # As this is an exception, we must handle it and finish the job.
        sys.exit(0)
    except:
        sys.stderr.write(colored('Cannot seem to begin; utterly confused & bailing out\n', 'red'))
        raise

    # Go
    try:
        print(colored('Gathering information...', 'blue', None, ['bold']))
        wanipz()
    except:
        sys.stderr.write(colored('Oh!\n', 'red'))
        raise
pass

if __name__ == '__main__':
    try:
        naime()
    except Exception as e:
        sys.stderr.write(colored('Hm, that did not work: {what} ({hint})\n', 'red', None, ['bold']).
            format(what=e, hint=type(e)))
        sys.exit(-1)
