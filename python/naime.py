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
from termcolor import colored
import subprocess
import argparse
import os
from pathlib import Path

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
        help(Path(ME).stem)
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

        with subprocess.Popen(external_cmd1,
                              stdin=None,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as p1:
            with subprocess.Popen(external_cmd2,
                                  stdin=p1.stdout,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as p2:
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
    except subprocess.CalledProcessError as e:
        print(colored('Cannot offload work to other commands!', 'red'), file=sys.stderr)
        print(colored('{because}', 'red').format(because=e.stderr.decode()), file=sys.stderr)
        raise
    except AssertionError:
        print(colored('Some of our guards fired!', 'red'), file=sys.stderr)
        raise

if __name__ == '__main__':
    try:
        naime()
    except Exception as e:
        print(colored('Hm, that did not work: {what} ({hint})', 'red', None, ['bold']).
            format(what=e, hint=type(e)), file=sys.stderr)
        sys.exit(-1)
    else:
        print(colored('Good, that went well...', 'green', None, ['bold']))
