import sys
import subprocess
import argparse
import re
from .downloader import (
    downloader_name,
    downloader_options,
)
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

def parse_cmd_line(me: str, purpose: str):
    """
    Read options, show help
    """
    try:
        parser = argparse.ArgumentParser(
            prog=me,
            description=purpose,
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

def naime(me: str, purpose: str):
    """
    Run the show
    """
    # Parse the command line
    try:
        args = parse_cmd_line(me, purpose)
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

    # Download
    try:
        for url in urls:
            print(colored('{url}', 'green', None, ['bold']).format(url=url))
        download(urls)
    except:
        raise

def download(urls):
    """
    Perform downloads
    """
    try:
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
