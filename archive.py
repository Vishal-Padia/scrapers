import os
import time
import internetarchive

# This is just a small POC, for fully fledged scraper, here's how it would work:
# We would use selenium to navigate to the webpage, click on the movies, then go to television (this is just an example, we could do anything),
# Then click on any one of the results, let's say the CNN San Francisco New, then it would have different videos, we could just grab the links of the videos
# Then use string manipulation to get the identifier of the video, then use the internetarchive library to download the video


def download_video(identifier, output_dir="downloads"):
    """
    Download a video from Internet Archive using their official API

    Args:
        identifier (str): The Internet Archive identifier for the item
        output_dir (str): Directory to save the downloaded file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get the item
        item = internetarchive.get_item(identifier)

        # Download the video file
        # By default, this will download the best quality version
        files = item.files
        video_files = [f for f in files if f["format"] in ["MPEG4", "h.264", "mp4"]]

        if video_files:
            file_name = video_files[0]["name"]
            print(f"Downloading: {file_name}")
            item.download(files=[file_name], destdir=output_dir, verbose=True)
        else:
            print("No video files found in this item")

    except Exception as e:
        print(f"Error downloading {identifier}: {str(e)}")


if __name__ == "__main__":
    # Example Usage
    identifier = "its_always_sunny_complete_archive"
    download_video(identifier)
