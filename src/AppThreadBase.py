from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import yt_dlp
from logging import log

""" Base class that only has knowledge of non-GUI libraries.
    Rationale: Decouples the logic from the GUI. This makes it easy to support a
    command-line version of your code later as well.
    
    https://stackoverflow.com/a/39694075/8765729 """


class AppThreadBase:
    def __int__(self, phook):
        super().__init__()
        self.phook = phook
        self.pool = ThreadPoolExecutor(max_workers=12)

    def download(self, yt_dlp_downloadable_links):
        pass

    def run(self, download_link, yt_dlp_options=None) -> int:
        if not yt_dlp_options:
            path = str(Path().cwd().resolve())
            yt_dlp_options = {
                "outtmpl": path + "/%(title)s.%(ext)s",
                "progress_hooks": [self.phook],
                "quiet": True,
                "no_warnings": True,
                "nocheckcertificate": True,
                "format": "best",
            }
        try:
            with yt_dlp.YoutubeDL(yt_dlp_options) as ydl:
                ydl.download(download_link)
        except yt_dlp.utils.DownloadError as ex:
            log.info(str(ex))
            return 1
        return 0
