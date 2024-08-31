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
            sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
            raise
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

    # Show dox about ourselves
    try:
        help(os.path.splitext(ME)[0])
    except:
        sys.stderr.write(colored('Cannot show beautified help; look at the source code!\n', 'red'))
        sys.stderr.write(colored("Or type '{me} --help' for more information.\n", 'red').
            format(me=ME))
        pass # We carry on!

    # Print the args found
    try:
        print(colored(args, 'green', None, ['bold']))
    except:
        sys.stderr.write(colored('Ugh!\n', 'red'))
        raise

    # Run a simple external command
    try:
        external_cmd = 'not false | wc --lines'
        result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
        print(colored('Truth consumes {output} lines', 'green').format(
            output=result.stdout.decode().strip()))
    except subprocess.CalledProcessError as e:
        sys.stderr.write(colored('Cannot offload work to other commands!\n', 'red'))
        sys.stderr.write(colored('{because}', 'red').format(because=e.stderr.decode()))
        raise
    except:
        sys.stderr.write(colored('Oh!\n', 'red'))
        raise
pass

if __name__ == '__main__':
    try:
        naime()
    except Exception as e:
        sys.stderr.write(colored('Hm, that did not work: {because}\n', 'red', None, ['bold']).
            format(because=str(type(e))))
        sys.exit(-1)
