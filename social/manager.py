from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time, random, sys
from users.manager import Manager as UserManager
platforms = {
    'THREADS': 'https://www.threads.net/login',
    'INSTAGRAM': 'https://www.instagram.com',
}

# geckodriver_path = '/opt/homebrew/bin/geckodriver'
# firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument(f'--webdriver={geckodriver_path}')

class Manager:
    def __init__(self, username, password, platform='INSTAGRAM', source_account='https://www.threads.net/@threads/'):
        self.driver = webdriver.Chrome()
        self.platform = platforms[platform]
        self.source_account = source_account
        self.username = username
        self.password = password
        self.accounts_followed = []
        self.modal_trigger = None
        self.modal = None
        self.sources = None
        self.total = 100

    def is_user(self):
        return UserManager.get(self.username) is not None
    
    def slow_type(self, element, text):
        # randdom delay between 2 keystrokes
        delay = random.uniform(0.001, 0.03)
        for char in text:
            element.send_keys(char)
            time.sleep(delay)
            
    def wait_random_time(self, min_seconds=2, max_seconds=15):
        wait_time = random.randint(min_seconds, max_seconds)
        for i in range(wait_time + 1):
            progress = "/" * i + "." * (wait_time - i)
            sys.stdout.write(f"[{progress}]\r")
            sys.stdout.flush()
            time.sleep(1)
        print()

    def go_to_platform(self):
        print('Going to platform')
        self.wait_random_time()
        try:
            # Open the website
            self.driver.get('https://www.instagram.com')

            # You can perform additional actions here if needed
        except Exception as e:
            self.driver.quit()
            # Print the exception if something went wrong
            print(e)
        # finally:
            # Close the browser window
            # self.driver.quit()

    def login(self):
        try:
            self.wait_random_time()
            # Find the input with type "text" and type the username
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            # type username into username input in 5 seconds
            
            # Find the input with type "password" and type the password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')

            # type into inputs
            self.slow_type(username_input, self.username)
            self.slow_type(password_input, self.password)

            # Find the element with inner text "Log in" and click on it
            login_button = self.driver.find_element(By.XPATH, '//*[text()="Log in"]')
            login_button.click()
        except Exception as e:
            print(e)
            self.driver.quit()


    def go_to_source_account(self):
        print('Going to source account')
        self.wait_random_time()
        
        try:
            self.driver.get(self.source_account)
        except Exception as e:
            print(e)
            self.driver.quit()

    def click_followers_modal(self):
        print('Clicking followers modal')
        self.wait_random_time()
        try:
            # Replace 'YourSubstring' with the desired substring of text
            substring = 'followers'

            # Use XPath to find the element containing the substring
            element_xpath = f'//*[contains(text(), "{substring}")]'
            self.modal_trigger = self.driver.find_element(By.XPATH, element_xpath)

            
            if self.modal_trigger:
                self.modal_trigger.click()
                print('Modal trigger clicked')
            else:
                print('Could not find the followers button')
                self.driver.quit()
        except Exception as e:
            print('Could not find the followers button')
            print(e)
            self.driver.quit()       
                
    def verify_modal_is_open(self):
        print('Opening follow modal')
        self.wait_random_time()
        # Find the element that contains the string of text "followers" and click on it
        try:
            
            # Find the modal element and wait for it to load
            modal_element = (By.CSS_SELECTOR, '[role="dialog"]')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(modal_element))
            print('Modal loaded')
            
            self.modal = self.driver.find_element(*modal_element)
            if self.modal:
                print('Modal found')
                self.get_accounts()
            else:
                print('Could not find the modal')
                self.driver.quit()
                
        except Exception as e:
            print(e)
            self.driver.quit()
        
    def move_mouse_to_element(self, element):
        actions = ActionChains(self.driver).move_to_element(element)
        actions.perform()


    def follow_accounts(self):
        print('Following accounts')
        try:
            for source in self.sources:
                # if we follow the max accounts, stop the loop
                if len(self.accounts_followed) >= self.total:
                    print('Followed max accounts, stopping')
                    break
                # if the amount followed is an increment of 10, take a break
                if len(self.accounts_followed) % 10 == 0:
                    print('Followed 10 accounts, taking a break')
                    self.wait_random_time(30, 60)
                    
                # find a button element with the role of button
                follow_button = source.find_element(By.CSS_SELECTOR, '[role="button"]')
                # move the mouse to the follow button
                follow_button.click()
                a_tag = source.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                href = href.rstrip('/')  # Use rstrip to remove trailing slash
                self.accounts_followed.append(href)
                print(f'Following {href}, accounts so far: {len(self.accounts_followed)}')
                self.wait_random_time()

        except Exception as e:
            print(e)
            self.driver.quit()

    def get_accounts(self):
        print('Getting accounts')
        self.wait_random_time()

        try:
            # find all the [data-pressable-container] = true elements
            self.sources = self.modal.find_elements(By.CSS_SELECTOR, '[data-pressable-container="true"]')

            if len(self.sources) > 0:
                self.follow_accounts()
            else:
                print('No accounts found to follow')
                self.driver.quit()
        
        except Exception as e:
            print(e)
            self.driver.quit()

    def close_modal(self):
        print('Closing modal')
        self.wait_random_time()

        try:
            # find the close button
            close_button = self.modal.find_element(By.CSS_SELECTOR, '[aria-label="Close"]')
            close_button.click()
            print('Modal closed')
        except Exception as e:
            print(e)
            self.driver.quit()
            
    def click_search(self):
        print('Clicking search')
        self.wait_random_time()

        try:
            # find the html element with the inner text 'Search'
            search_button = self.driver.find_element(By.XPATH, '//*[text()="Search"]')
            
            if search_button:
                print('Search found')
                search_button.click()
                print('Search clicked')
                
            else:
                print('Search not found')
                self.driver.quit()
                
        except Exception as e:
            print(e)
            self.driver.quit()
    def follow(self):
        self.go_to_platform()
        self.login()
        self.go_to_source_account()
        self.click_followers_modal()
        self.verify_modal_is_open()

        return True

    def ssend_messages(self, message):
        print('Sending messages')

        try:
            self.go_to_platform()
            self.login()
            self.go_to_source_account()
            
            self.wait_random_time()
            # find button that contains the partial text 'followers'
            b = self.driver.find_element(By.XPATH, '//*[contains(text(), "followers")]')
            
            if b:
                b.click()
                print('Followers button clicked')
            
            self.wait_random_time()
            
            try:
                # get the html element with a rold of dialog
                self.modal = self.driver.find_element(By.CSS_SELECTOR, '[role="dialog"]')

                self.wait_random_time()
                
                # find all the a tags with a class of notranslate
                links = self.modal.find_elements(By.CSS_SELECTOR, 'a.notranslate[role="link"]')
                print(f'Found {len(links)} links')
                
                for link in links:
                    print('Sending message')
                    print(link)
                    url = link.get_attribute('href')
                     # Open a new tab
                    ActionChains(self.driver) \
                        .key_down(Keys.CONTROL) \
                        .click(link) \
                        .key_up(Keys.CONTROL) \
                        .perform()

                    # Switch to the new tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])

                    # Go to the link
                    self.driver.get(url)

                    self.wait_random_time()

                    # Do whatever you need on the new tab



                    # get all buttons with a div  div 
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div div')
                    
                    # loop through the buttons and check if the text is 'Follow', if so, click it, and leave the buttons loop and go fnd the message button
                    for button in buttons:
                        if button.text == 'Follow':
                            button.click()
                            print('Follow button clicked')
                            self.wait_random_time()

                            continue
                        
                        # if the button text is 'Requested', close the tab and continue to the next link
                        if button.text == 'Requested':
                            print('Already requested')
                            # close the tab
                            self.driver.close()
                            
                            # switch back to the original tab
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            
                            # wait a random time
                            self.wait_random_time()
                            
                            # continue to the next link
                            continue
                        
                        # if the button text is 'Following', leave the buttons loop and continue to find the message button
                        if button.text == 'Following':
                            print('Already following')
                            break
                    
                    
                    # wait a random time
                    self.wait_random_time()
                    
                    # find the message button in the new tab of the clicked account
                    message_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Message")]')
                    
                    # if the message button is found, click it
                    if message_button:
                        message_button.click()
                        print('Message button clicked')
                        # wait for the mesage button click to change the page in the same new tab window
                        self.wait_random_time()


                        # find the input with the role of textbox 
                        message_input = self.driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')
                        send = self.driver.find_element(By.XPATH,
                                        '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')

                        # if message_input:
                        #     message_input.send_keys(message)
                        #     print('Message sent')
                        #     self.wait_random_time()
                        #     # find the button with the text 'Send'
                        #     send_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Send")]')
                            
                        #     if send_button:
                        #         send_button.click()
                        #         print('Send button clicked')
                        #         self.wait_random_time()
                                
                        #         # close the tab
                        #         self.driver.close()
                                
                        #         # switch back to the original tab
                        #         self.driver.switch_to.window(self.driver.window_handles[0])
                                
                        #         # wait a random time
                        #         self.wait_random_time()
                        #     else:
                        #         print('Could not find the send button')
                        #         self.driver.quit()
                        # else:
                        #     print('Could not find the message input')
                        #     self.driver.quit()
                    # else:
                    #     print('Could not find the message button')
                    #     # close the tab
                    #     self.driver.close()
                    #     # switch back to the original tab
                    #     self.driver.switch_to.window(self.driver.window_handles[0])
                        
                    #     # wait a random time
                    #     self.wait_random_time()
                        
                        # continue to the next link
                    continue
                    
            except Exception as e:
                print(e)
                self.driver.quit()
                
        except Exception as e:
            print(e)
            self.driver.quit()
    
    
            # except Exception as e:
            #         # close the tab
            #         self.driver.close()
            #         # switch back to the original tab
            #         self.driver.switch_to.window(self.driver.window_handles[0])
            #         # wait a random time
            #         self.wait_random_time()
            #         print('Follow button not clicked')
                    
                    # continue to the next link
    #                 continue
    #     except Exception as e:
    #         print(e)
    #         self.driver.quit()

    # except Exception as e:
    #     print(e)
    #     self.driver.quit()
        
    # return True
    def handle_private_account(self):
        try:
            # Wait for the 'Requested' button to appear, indicating that the follow request is sent
            requested_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Requested")]'))
            )
            print('Follow request sent. Account is private.')
        except TimeoutException:
            print('Error: Follow request not sent. Timeout reached.')

    def handle_follower_profiles(self, message):
        try:
            links = self.modal.find_elements(By.CSS_SELECTOR, 'a.notranslate[role="link"]')
            print(f'Found {len(links)} links')

            for link in links:
                url = link.get_attribute('href')

                # Open a new tab and switch to it
                ActionChains(self.driver) \
                    .key_down(Keys.CONTROL) \
                    .click(link) \
                    .key_up(Keys.CONTROL) \
                    .perform()

                self.driver.switch_to.window(self.driver.window_handles[-1])

                # Check if the account is private and handle accordingly
                if self.is_private_account():
                    self.handle_private_account()
                else:
                    # Follow and send message
                    self.handle_follower_profile(url, message)

                # Close the current tab to switch back
                self.driver.close()

                # Switch back to the original tab
                self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            print(f'Error while handling follower profiles: {e}')

     
    def send_messages(self, message):
        try:
            self.go_to_platform()
            self.login()
            self.go_to_source_account()
            self.click_followers_modal()
            self.verify_modal_is_open()

            # Handle follower profiles
            self.handle_follower_profiles(message)
        except Exception as e:
            print(f'Error in send_messages: {e}')
        finally:
            self.driver.quit()

        return True


    def is_already_following(self):
        try:
            follow_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Following")]')
            return follow_button is not None
        except NoSuchElementException:
            return False

    def follow_and_send_message(self, message):
        try:
            follow_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Follow")]')
            follow_button.click()
            self.wait_random_time()

            # Check if the account is private and follow request is sent
            if self.is_private_account():
                print('Follow request sent. Account is private.')
                return

            # Account is not private, proceed to sending a direct message
            self.send_direct_message(message)
        except Exception as e:
            print(f'Error while following: {e}')

    def send_direct_message(self, message):
        try:
            message_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Message")]')
            message_button.click()
            self.wait_random_time()

            # Find the input field for typing the message
            message_input = self.driver.find_element(By.CSS_SELECTOR, '[role="textbox"]')

            # Type the message and send it
            self.slow_type(message_input, message)
            send_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Send")]')
            send_button.click()

            print('Message sent successfully.')
        except Exception as e:
            print(f'Error while sending a message: {e}')

    def is_private_account(self):
        try:
            # Check if the follow button changes to 'Requested' indicating a private account
            requested_button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Requested")]')
            return requested_button is not None
        except NoSuchElementException:
            return False


    def handle_follower_profile(self, url, message):
        # Open a new tab
        ActionChains(self.driver) \
            .key_down(Keys.CONTROL) \
            .click(url) \
            .key_up(Keys.CONTROL) \
            .perform()

        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # Check if already following
        if self.is_already_following():
            self.send_direct_message(message)
        else:
            self.follow_and_send_message(message)

        # Close the current tab to switch back
        self.driver.close()

        # Switch back to the original tab
        self.driver.switch_to.window(self.driver.window_handles[0])





