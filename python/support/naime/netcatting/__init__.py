import textwrap
import asyncio
import sys
from subprocess import (
    PIPE,
    Popen,
)
from support.pathorstr import (
    PathOrStr,
)
async def do_netcatting(prog: PathOrStr='nc', host: str='localhost', port: str=None) -> None:
    """
    Let us attempt to feed this netcat command a here-document.  Tcpdump with -XX to localhost and
    the UDP port given to verify that leading indentation is not an issue:
    """
    nc_cmd = [
        prog,
            '--verbose',
            '--udp',
            '--send-only',
            host,
            port
    ]
    try:
        nc_here_doc = textwrap.dedent('''
            This
            That
            The other
                And everything above
        ''').lstrip().encode()

        for _ in range(5):
            print('Sending packet...', end='')
            with Popen(nc_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE) as nc:
                outs, errs = nc.communicate(nc_here_doc)
            await asyncio.sleep(1)
            assert nc.returncode == 0
            print('Ok')
        print('The length of here-doc is {this}'.format(this=len(nc_here_doc)))
    except:
        print('Something went wrong with the command: {cmd}'.format(cmd=nc_cmd), file=sys.stderr)
        print('Trying to execute:', nc_here_doc.decode(), sep='\n', end='', file=sys.stderr)
        raise
