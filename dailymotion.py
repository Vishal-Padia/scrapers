# This is a two-step process
# The first step of the process would be to get the video url from the dailymotion website (which I am skipping in this PoC)
# The second step of the process would be to use selenium to navigate to the "https://en.savefrom.net" or "Vid Burner" or "https://www.savethevideo.com/", paste the video url, and download the video

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions

BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"


class DailymotionScraper:
    """
    A class to download videos from dailymotion
    """

    def __init__(self, brave_path=BRAVE_PATH):
        """
        Initializes the DailymotionScraper with Brave browser options.
        """
        self.options = ChromeOptions()
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-gpu")
        self.options.binary_location = brave_path
        self.driver = webdriver.Chrome(options=self.options)

    def download_video(self, video_url):
        """
        Downloads the video from the given video URL
        """
        print("Navigating to Vid Burner")
        self.driver.get("https://vidburner.com/")
        time.sleep(5)

        print("Pasting video URL")
        search_box = self.driver.find_element(By.ID, "url")
        search_box.send_keys(video_url)
        search_box.send_keys(Keys.RETURN)

        time.sleep(10)

        # need to find a better way to do find the download link, but this works as of now
        download_link = self.driver.find_element(
            By.XPATH, '//*[@id="result"]/div/div/div[1]/div/div[2]/a[2]'
        )
        download_link.click()
        time.sleep(10)

        # check if there's a pop-up
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
        except:
            pass

        # PS you'll have to manually give the location to where you want to save the video (this can be done by setting download location while initalizing the browser)
        print("Video downloaded successfully")


if __name__ == "__main__":
    # Example Usage
    video_url = "https://www.dailymotion.com/video/x9dpma6"
    dailymotion_scraper = DailymotionScraper()
    dailymotion_scraper.download_video(video_url)
