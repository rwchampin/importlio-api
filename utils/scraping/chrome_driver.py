from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver_location = '/opt/homebrew/bin/chromedriver'
search_key = 'AIzaSyBXVuHN8e_8ZytTu9SwqcuRyiOIelHYXhA'

# add proxy to selenium
    # proxy = '19.33.33.33'
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=%s' % proxy)
    
    driver = webdriver.Chrome(chrome_driver_location)
    
# scraper class to init chrome driver and have fn to scrape url w proxy
class Scraper:
    def __init__(self):
        # init chrome driver
        self.driver = webdriver.Chrome(chrome_driver_location)
        
    def scrape_url(self, url):
        # get the url
        self.driver.get(url)
        
        # get the body html
        body = self.driver.find_element_by_tag_name('body').text
        
        # return the body html
        return body