import time
import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Constants
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
DOWNLOAD_PATH = "downloads"  # Directory to save videos


class YoutubeScraper:
    """
    A class to scrape YouTube video links and download videos.
    """

    def __init__(self, brave_path=BRAVE_PATH):
        """
        Initializes the YoutubeScraper with Brave browser options.
        """
        self.options = ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.binary_location = brave_path
        self.driver = webdriver.Chrome(options=self.options)

    def youtube_video_link_grabber(self, query, num_scrolls=2):
        """
        Navigates to YouTube, scrolls to load videos, and extracts video links.

        Args:
            query (str): Search query for YouTube.
            num_scrolls (int): Number of times to scroll down.

        Returns:
            list: A list of video links.
        """
        print("Navigating to YouTube with query:", query)
        self.driver.get(f"https://www.youtube.com/search?q={query}")

        print("Waiting for the page to load")
        time.sleep(5)

        for i in range(num_scrolls):
            print(f"Scrolling down {i+1}/{num_scrolls}")
            self.driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )  # Scroll to bottom
            time.sleep(3)

        print("Getting video links")
        try:
            video_elements = self.driver.find_elements(By.ID, "video-title")
            print(f"Found {len(video_elements)} video elements")
            video_links = [
                video.get_attribute("href")
                for video in video_elements
                if video.get_attribute("href")
            ]
            print(f"Extracted {len(video_links)} valid video links")
        except Exception as e:
            print(f"Error getting video elements: {e}")
            return []

        return video_links

    def download_video(self, video_link, output_path=DOWNLOAD_PATH):
        """
        Downloads a video using yt_dlp.

        Args:
            video_link (str): URL of the video to download.
            output_path (str): Directory to save the downloaded video.
        """
        ydl_opts = {
            "format": "best",
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading {video_link}")
                ydl.download([video_link])
                print(f"Downloaded {video_link}")
        except Exception as e:
            print(f"Error downloading {video_link}: {e}")

    def close(self):
        """
        Closes the Selenium WebDriver.
        """
        print("Closing the browser")
        self.driver.quit()


if __name__ == "__main__":
    # Example Usage
    search_query = "Ted Talks"
    scraper = YoutubeScraper()  # Using default Brave path

    try:
        video_links = scraper.youtube_video_link_grabber(search_query)

        if video_links:
            print(f"Found {len(video_links)} video links:")
            for link in video_links:
                print(link)
                scraper.download_video(link)
        else:
            print("No video links found.")
    finally:
        scraper.close()  # Ensure the driver is closed even if errors occur
