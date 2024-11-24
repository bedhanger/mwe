from asyncio import (
    create_subprocess_exec as ampersand,
)
from asyncio.subprocess import (
    Process as Job,
)
async def do_tcpdumping() -> Job:
    """
    Create tcpdump as a subprocess in the "background"
    Note that you should make provisions to run tcpdump rootless beforehand
    Adapt interface and BPF rule as you see fit
    """
    return await ampersand(
        'tcpdump',
            '--interface=lo',
            'udp port 49123',
            # This does **not** buffer IO
            '--packet-buffered'
    )
