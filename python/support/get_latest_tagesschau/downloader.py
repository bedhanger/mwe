import subprocess

def download(urls):
    """
    Perform downloads
    """
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
