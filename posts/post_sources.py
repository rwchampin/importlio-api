from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
from selenium.common.exceptions import NoSuchElementException

class PostManager:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.source = 'https://www.autods.com/blog/'
    
    def wait_random_time(self):
        # wait random time
        print('Waiting random time...')
        time.sleep(1)
        print('Done waiting random time.')
        
    def get(self):
        # get post data from URL
        self.driver.get(self.source)
        
        # wait random time
        self.wait_random_time()
        
        scroll = True
        
        try:
            while scroll:
                # scroll to the bottom of the page
                # self.driver.find_element("body").send_keys(Keys.END)

                try:
                    # find button with id show-btn
                    show_more_button = self.driver.find_element(By.ID, "show-btn")

                    if not show_more_button.is_displayed():
                        scroll = False
                        break
                    # click button
                    show_more_button.click()
                    
                    # wait random time
                    self.wait_random_time()
                except NoSuchElementException:
                    scroll = False
            
            print('No more posts to show.')       
            
            # get all html elements with class post
            import pdb; pdb.set_trace()
            
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the WebDriver
            pass

# Create an instance of PostManager and call the get method
