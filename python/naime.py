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
        help(os.path.splitext(ME)[0])
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

    # Run a simple external command
    try:
        external_cmd = 'not false | wc --lines'
        result = subprocess.run(external_cmd, check=True, shell=True, capture_output=True)
        print(colored('Truth consumes {output} lines', 'green').format(
            output=result.stdout.decode().strip()))
    except subprocess.CalledProcessError as e:
        print(colored('Cannot offload work to other commands!', 'red'), file=sys.stderr)
        print(colored('{because}', 'red').format(because=e.stderr.decode()), file=sys.stderr)
        raise
    except:
        print(colored('Oh!', 'red'), file=sys.stderr)
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
