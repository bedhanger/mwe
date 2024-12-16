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
