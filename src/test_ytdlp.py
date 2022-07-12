import yt_dlp


def download(videos: list[str]):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(videos)


def test_simple_yt_dlp():
    test = ['https://www.youtube.com/watch?v=BaW_jenozKc']
    download(test)
