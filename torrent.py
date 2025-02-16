# This is a two-step process
# The first step of the process would be to use selenium to get the torrent magnet link from the torrent website
# The second step of the process would be to use the library to download the torrent

import time
from selenium import webdriver
from torrentp import TorrentDownloader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions

DOWNLOAD_PATH = "downloads"
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"


class TorrentDownloader:
    """
    A class to download torrents from torrent websites
    """

    def __init__(self, brave_path=BRAVE_PATH):
        """
        Initializes the TorrentDownloader with Brave browser options.
        """
        self.options = ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.binary_location = brave_path
        self.driver = webdriver.Chrome(options=self.options)

    def get_the_magnet_url(self, query):
        """
        Navigate to the torrent website and get the magnet link
        """
        print("Navigating to the torrent website")
        self.driver.get("https://www.1337x.pro")
        time.sleep(5)

        print("Searching for the torrent")
        search_box = self.driver.find_element(By.ID, "autocomplete")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)
        print("Getting the first search result")
        # go through the search results with class torsearch and get the first one
        search_results = self.driver.find_elements(By.CLASS_NAME, "torsearch")
        first_result = search_results[0]
        first_result.click()

        time.sleep(5)

        print("Getting the magnet link")
        magnet_link = self.driver.find_element(
            By.XPATH, "/html/body/main/div/div/div/div[2]/div[1]/ul[1]/li[1]/a"
        )
        # get the href link
        magnet_link = magnet_link.get_attribute("href")

        return magnet_link

    def download_torrent(self, magnet_link):
        """
        Download the torrent using the magnet link
        """
        print("Downloading the torrent")
        torrent = TorrentDownloader()
        torrent.download(magnet_link, DOWNLOAD_PATH)
        print("Torrent downloading....")
        time.sleep(5)
        torrent.stop()
        print("Torrent download stopped")


if __name__ == "__main__":
    # Example Usage
    query = "The Shawshank Redemption"
    torrent = TorrentDownloader()
    magnet_link = torrent.get_the_magnet_url(query)
    print(magnet_link)
    torrent.download_torrent(magnet_link)
