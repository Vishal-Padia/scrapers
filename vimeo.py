# There's library for this
# But still, this would be a two-step process
# The first step would be to get the video url from the vimeo website (which I am skipping in this PoC)
# The second step would be to use the library to download the video

import os
from vimeo_downloader import Vimeo

DOWNLOAD_PATH = "downloads"


def download(video_url):
    """
    Download a video from Vimeo using the vimeo_downloader library

    Args:
        video_url (str): The Vimeo video URL
    """
    try:
        v = Vimeo(video_url)
        # get the highest quality stream
        video_stream = v.streams[-1]
        video_stream.download(
            download_directory=DOWNLOAD_PATH, filename=v.metadata.title
        )
        print(f"Downloaded {video_url}")
    except Exception as e:
        print(f"Error downloading {video_url}: {e}")


video_url = "https://vimeo.com/440801455"
download(video_url)
