from concurrent.futures import ThreadPoolExecutor as Pool
from pathlib import Path
import yt_dlp

#  Seperate this into a class.
# It still uses QtWorkers


pool = Pool()


def pHook(d):  # yt-dlp callback
    if d["status"] == "downloading":
        print("downloading ... ")
    if d["status"] == "finished":
        print("download completed")


def run(download_link, yt_dlp_options=None) -> int:
    if not yt_dlp_options:
        path = str(Path().cwd().resolve())
        yt_dlp_options = {
            "outtmpl": path + "/%(title)s.%(ext)s",
            "progress_hooks": [pHook],
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


def main():
    links = [
        "https://www.youtube.com/watch?v=DpdurQPpR4U",
        "https://www.youtube.com/watch?v=kljPffFTRqw",
        "https://www.youtube.com/watch?v=8THfV6qb2dU",
    ]
    # sequential exectuion
    for link in links:
        run(link)


if __name__ == "__main__":
    main()
