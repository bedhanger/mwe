from asyncio import (
    create_subprocess_exec as ampersand,
)
from asyncio.subprocess import (
    Process as Job,
)
from support.pathorstr import (
    PathOrStr,
)
async def do_tcpdumping(prog: PathOrStr='tcpdump', nic: str=None, fltr_expr: str=None) -> Job:
    """
    Create tcpdump as a subprocess in the "background"
    Note that you should make provisions to run tcpdump rootless beforehand
    """
    # Despite the name of the literal param, it does **not** buffer IO
    return await ampersand(prog, '--packet-buffered', nic, fltr_expr)
