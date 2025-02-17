#!/usr/bin/env python
"""
Before rewriting from scratch the "bare minimum of every Python script," here is a template of
sorts.

It has a __main__ guard, shows docu about itself (you're reading it right now), sports the beginning
of command line processing, and loads some work off to an external command.  All of this is
cushioned in exception handling.  And it colours the "diagnostix" it emits!

The name is an intentional misspelling of the amalgamation of "name and main".
"""
import sys
try:
    from termcolor import colored
except ModuleNotFoundError:
    def colored(_, *pargs, **kwargs):
        return _
from subprocess import Popen, PIPE, CalledProcessError
import argparse
from pathlib import Path, PurePath
import asyncio

from support.naime.netcatting import (
    do_netcatting,
)
from support.naime.tcpdumping import (
    do_tcpdumping,
)

async def naime():
    """
    Run the show
    """
    # Identify ourselves
    ME = PurePath(__file__).name

    def parse_cmd_line():
        """
        Read options, show help
        """
        try:
            parser = argparse.ArgumentParser(
                prog=ME,
                description=__doc__,
                epilog='Save this under a different name and start developing from there.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            parser.add_argument(
                'some_arg',
                type=str,
                nargs='*',
                default='some_default',
                help='some help',
            )
            return parser.parse_args()
        except argparse.ArgumentError:
            print(colored('Could not decipher the command line', 'red'), file=sys.stderr)
            raise

    # Parse the command line
    try:
        args = parse_cmd_line()
    except SystemExit:
        # When the user requested help, the arg parser displays it and concludes with a sys.exit(0).
        # As this is an exception, we must handle it and finish the job.
        sys.exit(0)
    except:
        print(colored('Cannot seem to begin; utterly confused & bailing out', 'red'),
              file=sys.stderr)
        raise

    # Show dox about ourselves
    try:
        help(Path(ME).name)
    except:
        print(colored('Cannot show beautified help; look at the source code!', 'red'),
              file=sys.stderr)
        print(colored("Or type '{me} --help' for more information.", 'red').
            format(me=ME), file=sys.stderr)
        pass # We carry on!

    # Print the args found
    try:
        print(colored(args, 'green', None, ['bold']))
    except:
        print(colored('Ugh!', 'red'), file=sys.stderr)
        raise

    # Run two simple external commands connected via a pipe; there is no shell support.
    # We expect a single line of output.
    try:
        external_cmd1 = ['/bin/true']
        external_cmd2 = ['wc', '--lines']

        with Popen(external_cmd1, stdin=None, stdout=PIPE, stderr=PIPE) as p1:
            with Popen(external_cmd2, stdin=p1.stdout, stdout=PIPE, stderr=PIPE) as p2:
                raw_stdout, raw_stderr = p2.communicate()
                output,     errors     = raw_stdout.decode(), raw_stderr.decode()

        # Now check some properties
        assert p1.returncode == 0, '"Command" {command} is unhappy'.format(command=external_cmd1)
        assert p2.returncode == 0, '"Command" {command} is unhappy'.format(command=external_cmd2)
        assert output.count('\n') == 1, 'There is an unexpected number of lines in the output'
        assert output == '0\n', '"{this}" is not what we want to see'.format(this=output.strip())
        assert errors == '', 'Errors occurred: "{oops}"'.format(oops=errors.strip())

        # Finally, output the result
        print(colored('Truth consumes {so_many} lines', 'green').format(so_many=output.strip()))
    except CalledProcessError as e:
        print(colored('Cannot offload work to other commands!', 'red'), file=sys.stderr)
        print(colored('{because}', 'red').format(because=e.stderr.decode()), file=sys.stderr)
        raise
    except AssertionError:
        print(colored('Some of our guards fired!', 'red'), file=sys.stderr)
        raise

    try:
        print('Tcpdump and netcat simultaneously')
        the_port = 49123

        tcpdumping = await do_tcpdumping(
            prog='tcpdump',
            nic='--interface=lo',
            fltr_expr='udp port {port}'.format(port=the_port),
        )
        print('Running tcpdump as PID {pid}'.format(pid=tcpdumping.pid))

        await do_netcatting(
            prog='ncat',
            host='localhost',
            port=str(the_port)
        )

        # Netcat's done when we are done netcatting, so we only worry about tcpdump
        print('Asking tcpdump to shut down...', end='')
        tcpdumping.terminate()
        print('Ok')
    except:
        print(colored('Juggling two jobs & the main routine did not work.', 'red'), file=sys.stderr)

if __name__ == '__main__':
    sys.exit(asyncio.run(naime()))
