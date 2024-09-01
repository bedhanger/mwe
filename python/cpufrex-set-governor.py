#!/usr/bin/env python
"""
Set the CPU frequency governing policy.
"""
import sys
from termcolor import colored

class GovernorNotAvailableError(Exception): pass
class CpuNotFoundError(FileNotFoundError): pass

def naime():
    """
    Run the show
    """
    def parse_cmd_line():
        """
        Read options, show help
        """
        import argparse
        import os

        # Identify ourselves
        ME = os.path.basename(__file__)

        try:
            parser = argparse.ArgumentParser(
                prog=ME,
                description=__doc__,
                epilog='You may need to load additional kernel modules to get more governors.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            parser.add_argument(
                'governor',
                type=str,
                nargs='?',
                default='powersave',
                help='the new frequency governor that will be used for all CPUs found',
            )
            parser.add_argument(
                '-l', '--list-governors',
                action='store_true',
                help='just show the currently available frequency governors',
            )
            parser.add_argument(
                '-v', '--verbose',
                action='store_true',
                help='be chatty about what gets done',
            )
            parser.add_argument(
                '-c', '--reference-cpu',
                type=int,
                default=0,
                help='id of the CPU to obtain the list of available governors',
            )
            return parser.parse_args()
        except argparse.ArgumentError:
            sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
            raise
    pass

    def get_available_governors(from_cpu):
        """
        Produce the list of currently known governors
        """
        try:
            with open('/sys/devices/system/cpu/cpu{the_cpu}/cpufreq/scaling_available_governors'.
                format(the_cpu=from_cpu) , 'r') as reference_cpu_file:
                    return reference_cpu_file.read().rstrip()
        except FileNotFoundError:
            raise CpuNotFoundError('CPU{cpu}: no such device'.format(cpu=from_cpu))
        except:
            sys.stderr.write(colored(
                'Could not determine scaling governor availability (from CPU{cpu})\n', 'red').
                    format(cpu=from_cpu))
            raise
    pass

    def list_the_governors(available_governors=None, verbose=False):
        """
        Show which ones can be selected from
        """
        the_list = available_governors.split(' ')
        print(colored(the_list, 'green')) if verbose else None
        return the_list
    pass

    def set_new_governor(new_governor, verbose=False):
        """
        Ѕet it for all CPUs found
        """
        import glob

        if verbose:
            print(colored('Will attempt to set "{gov}" as the new governor', 'green').
                format(gov=new_governor))

        scaling_govs = glob.glob('/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor')
        if verbose:
            print(colored('Found {this_many} governors to set', 'green').format(
                this_many=len(scaling_govs)))

        for scaling_gov in scaling_govs:
            if verbose:
                print(colored('Working on {gov}', 'green').format(gov=scaling_gov))
                with open(scaling_gov, 'r') as f:
                    current_governor = f.read().rstrip()
                    print(colored('Trying to establish "{new_gov}" as the new governor ', 'green').
                        format(new_gov=new_governor)
                        + colored('(replacing "{old_gov}")', 'green').format(
                            old_gov=current_governor, new_gov=new_governor))
            try:
                with open(scaling_gov, 'w') as f:
                    assert f.write('{what}'.format(what=new_governor)) == len(new_governor)
            except PermissionError:
                sys.stderr.write(colored('You appear to not have the privileges to set a new governor\n', 'red'))
                raise
            except AssertionError:
                sys.stderr.write(colored('Unable to set "{gov}" as the new governor\n', 'red').
                    format(gov=new_governor))
                raise
    pass

    try:
        args = parse_cmd_line()
        new_governor = args.governor
        verbose = args.verbose
        list_governors = args.list_governors
        reference_cpu = args.reference_cpu
    except SystemExit:
        # When the user requested help, the arg parser displays it and concludes with a sys.exit(0).
        # As this is an exception, we must handle it and finish the job.
        sys.exit(0)
    except:
        sys.stderr.write(colored('Cannot seem to begin; utterly confused & bailing out\n', 'red'))
        raise

    try:
        available_governors = get_available_governors(from_cpu=reference_cpu)
        if verbose:
            print(colored('Found these governors to be available (as reported by CPU{cpu}): {govs}',
                'green').format(govs=available_governors, cpu=reference_cpu))
    except:
        sys.stderr.write(colored('Could not assemble list of available governors\n', 'red'))
        raise

    if list_governors:
        try:
            list_of_available_govs = list_the_governors(available_governors, verbose=verbose)
            if verbose:
                print(colored('These are the governors you can choose from:', 'green'))
            for available_governor in list_of_available_govs:
                print(available_governor)
            return
        except:
            sys.stderr.write(colored('Could not display list of available governors\n', 'red'))
            raise

    if new_governor in available_governors:
        try:
            set_new_governor(new_governor, verbose)
            print(colored('Set "{new_governor}" as the new governor', 'green', None, ['bold']).
                format(new_governor=new_governor))
        except:
            sys.stderr.write(colored('Governor "{gov}" could not be set\n', 'red').
                format(gov=new_governor))
            raise
    else:
        sys.stderr.write(colored('Governor "{gov}" is currently not available\n', 'red').
            format(gov=new_governor))
        sys.stderr.write(colored('Choose one from the list of {available_ones}\n', 'red').
            format(available_ones=list_the_governors(available_governors)))
        raise GovernorNotAvailableError('Unknown governor')
pass

if __name__ == '__main__':
    try:
        naime()
    except Exception as the_problem:
        sys.stderr.write(colored('Hm, that did not work: {what} ({hint})\n', 'red', None, ['bold']).
            format(what=the_problem, hint=type(the_problem)))
        sys.exit(-1)
