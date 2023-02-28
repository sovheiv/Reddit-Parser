from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selenium import webdriver

from PiiQMedia.settings import PARSER
import logging

logger = logging.getLogger(__name__)


class RedditParser:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()
        if headless:
            options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")

        ser = Service(PARSER["DRIVER_PATH"])

        self.driver = webdriver.Chrome(service=ser, options=options)

        self.driver.maximize_window()

    def get_post_data(self, url: str):
        self.driver.get(url)

        if not self.wait_post_load():
            return False

        post_container = self.driver.find_element(
            by=By.XPATH, value="//div[@data-testid='post-container']"
        )

        title = post_container.find_element(by=By.CLASS_NAME, value=PARSER["TITLE_CLASS"]).text
        text_parts = post_container.find_elements(
            by=By.CLASS_NAME, value=PARSER["CONTENT_PART_CLASS"]
        )
        text = "\n".join([part.text for part in text_parts])

        likes_num = self.driver.find_element(
            by=By.XPATH, value=f"//*[starts-with(@id, '{PARSER['LIKES_ID_START']}')]"
        ).text
        comments_num = post_container.find_element(
            by=By.CLASS_NAME, value=PARSER["COMMENTS_CLASS"]
        ).text.split()[0]

        return {
            "url": url,
            "content": {"title": title, "text": text},
            "likes_num": self.format_num(likes_num),
            "comments_num": self.format_num(comments_num),
        }

    @staticmethod
    def format_num(num: str):
        if num.isdigit():
            return int(num)
        if num.endswith("k") or num.endswith("K"):
            return int(float(num[:-1]) * 1000)
        if num.endswith("m") or num.endswith("M"):
            return int(float(num[:-1]) * 1000000)

        logger.error(f"Wrong number: {num}")
        return False

    def wait_post_load(self):
        try:
            post_end = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, PARSER["POST_END_CLASS"]))
            )
            actions = ActionChains(self.driver)
            actions.move_to_element(post_end).perform()
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, PARSER["CONTENT_PART_CLASS"]))
            )
            return True
        except TimeoutException:
            return False
