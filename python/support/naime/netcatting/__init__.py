import textwrap
import asyncio
import sys
from subprocess import (
    CalledProcessError,
    PIPE,
    Popen,
)

async def do_netcatting() -> None:
    """
    Let us attempt to feed this netcat command a here-document.  Tcpdump with -XX to localhost and
    the UDP port given to verify that leading indentation is not an issue:
    """
    nc_cmd = ['nc', '--verbose', '--udp', '--send-only', 'localhost', '49123']
    try:
        nc_here_doc = textwrap.dedent('''
            This
            That
            The other
        ''').lstrip().encode()

        with Popen(nc_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE) as nc:
            outs, errs = nc.communicate(nc_here_doc)
        assert nc.returncode == 0
        print('The length of here-doc is {this}'.format(this=len(nc_here_doc)))
    except:
        print('Something went wrong with the command: {cmd}'.format(cmd=nc_cmd), file=sys.stderr)
        print('Trying to execute:', nc_here_doc.decode(), sep='\n', end='', file=sys.stderr)
        raise
