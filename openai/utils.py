import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class WebScraper:
    def __init__(self, url, button_xpath):
        self.url = url
        self.button_xpath = button_xpath
        self.driver = None

    def setup_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def click_button(self):
        show_more_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.button_xpath))
        )
        show_more_button.click()

    def scrape_page(self):
        self.setup_driver()
        self.driver.get(self.url)

        while True:
            try:
                self.click_button()
                time.sleep(2)
            except:
                break

        page_html = self.driver.page_source
        self.driver.quit()

        soup = BeautifulSoup(page_html, 'html.parser')
        return soup.prettify()


