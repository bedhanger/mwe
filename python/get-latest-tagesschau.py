#!/usr/bin/env python
"""
Utilise Youtube downloader.  Get the most recent Tagesschau by default.
"""
import sys
from termcolor import colored
import subprocess
import argparse
from pathlib import PurePath
import re

def naime():
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

    def upgrade_to_https(urls):
        """
        Replace HTTP protocol specifier in favour of HTTPS.
        Lowercase the result in this case.
        """
        new_urls = []
        http = re.compile(r"^(http)(://)", re.IGNORECASE)
        for url in urls:
            try:
                match = re.search(http, url)
                assert match is not None
                https = match.group(1).lower() + 's' + match.group(2)
                url = re.sub(http, https, url)
            except AssertionError:
                # Just didn't start with http://
                # Nevermind!
                pass
            finally:
                new_urls.append(url)
        return new_urls
    pass

    def upgrade_to_webxxl(urls):
        """
        Super-size me!
        """
        new_urls = []
        small = re.compile(r"(\.web)x?(l|s)\.\b", re.IGNORECASE)
        for url in urls:
            try:
                match = re.search(small, url)
                assert match is not None
                big = match.group(1) + 'xxl.'
                url = re.sub(small, big, url)
            except AssertionError:
                # Nevermind!
                pass
            finally:
                new_urls.append(url)
        return new_urls
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
        urls = upgrade_to_https(urls)
    except:
        raise

    # Try to go for the web XXL version
    try:
        urls = upgrade_to_webxxl(urls)
    except:
        raise

    for url in urls:
        print(colored('{url}', 'green', None, ['bold']).format(url=url))

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
        result = subprocess.run(downloader_cmd, check=True, shell=True)
    except subprocess.CalledProcessError:
        sys.stderr.write(colored('Cannot download!\n', 'red'))
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
