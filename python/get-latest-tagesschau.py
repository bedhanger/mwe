#!/usr/bin/env python
"""
Utilise Youtube downloader.  Get the most recent Tagesschau by default.
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
                epilog=None,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
            parser.add_argument(
                'urls',
                nargs='*',
                default=['https://www.tagesschau.de/export/video-podcast/webxl/tagesschau'],
                help='the URLs to retrieve',
            )
            return parser.parse_args()
        except argparse.ArgumentError:
            sys.stderr.write(colored('Could not decipher the command line\n', 'red'))
            raise
    pass

    # Parse the command line
    try:
        args = parse_cmd_line()
        urls = args.urls
    except SystemExit:
        # When the user requested help, the arg parser displays it and concludes with a sys.exit(0).
        # As this is an exception, we must handle it and finish the job.
        sys.exit(0)
    except:
        sys.stderr.write(colored('Cannot seem to begin; utterly confused & bailing out\n', 'red'))
        raise

    # Upgrade to https
    try:
        for url in urls:
            print(colored('{url}', 'green', None, ['bold']).format(url=url))
            # TODO: upgrade!
    except:
        raise

    # Download
    try:
        downloader_name = 'yt-dlp'
        downloader_options = [
            '--playlist-items=1',
            '--no-part',
            '--restrict-filenames',
            '--fixup never',
            '--format="(xl_mp4/mp4)"',
            '--socket-timeout=600',
            '--concurrent-fragments=12',
            '--ignore-errors',
        ]
        downloader_cmd = '{downloader_name} {downloader_options} {urls}'.format(
            downloader_name=downloader_name, downloader_options=' '.join(downloader_options),
            urls=' '.join(urls))
        result = subprocess.run(downloader_cmd, check=True, shell=True, capture_output=False)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(colored('Cannot download!\n', 'red'))
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
        sys.stderr.write(colored('Hm, that did not work: {what} ({hint})\n', 'red', None, ['bold']).
            format(what=e, hint=type(e)))
        sys.exit(-1)

# TODO
## Go for the .webxxl. version if .web(l|s). is offered.
#WHAT_TO_GET=$(perl -p -e 's/(\.web)(l|s)\.\b/\1xxl./' <<< ${WHAT_TO_GET})
