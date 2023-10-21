import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import json
import time, random
import re
chrome_driver_location = '/opt/homebrew/bin/chromedriver'
search_key = 'AIzaSyBXVuHN8e_8ZytTu9SwqcuRyiOIelHYXhA'

username = "geonode_y52krAfiwj-country-US"
password = "685d0e68-e072-473e-86c0-beae004f73e3"
GEONODE_DNS = "rotating-residential.geonode.com:9000"


# Function to remove HTML tags from a string
def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    # soup = re.sub('[^A-Za-z0-9]+', '', str(soup))
    import pdb; pdb.set_trace()
    return soup.get_text()

# Function to extract emails from a text string
def extract_emails(text):
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
    import pdb; pdb.set_trace()
    return emails


def get_proxy():
    return {"http":"http://{}:{}@{}".format(username, password, GEONODE_DNS)}

def scrape_google_search():
    page = 0
    results_per_page = 100
    
    
    
    url = "https://www.google.com/search?q=+%22fitness+instructor%22%20AND%20%22%40gmail.com%22%20-intitle:%22profiles%22%20-inurl:%22dir/+%22+site:www.linkedin.com/in/+OR+site:www.linkedin.com/pub/&start={}&num={}".format(page, results_per_page)   
    PROXY = get_proxy()
    
    # add proxy to requests
    response = requests.get(url, proxies=PROXY)
    
    if(response.status_code == 200):
        # make soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # get body html
        body = soup.find("body").text
        
        # find the html elements with the text "linkedin.com"
        linkedin_elements = soup.find_all(text=re.compile("linkedin.com"))
        
        # get a count of the number of linkedin elements
        linkedin_element_count = len(linkedin_elements)
        
        # print and return the count
        print(linkedin_element_count)

        return body
        
    else:
        print("Error:", response.status_code)
        return None
    
    
    # add proxy to selenium
    # proxy = '19.33.33.33'
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--proxy-server=%s' % proxy)
    
    driver = webdriver.Chrome(chrome_driver_location)
    if url is None:
        url = "https://www.google.com/search?q=+%22fitness+instructor%22%20AND%20%22%40gmail.com%22%20-intitle:%22profiles%22%20-inurl:%22dir/+%22+site:www.linkedin.com/in/+OR+site:www.linkedin.com/pub/"
    try:
        # Open the URL in the browser
        driver.get(url)

        def scroll_to_bottom():
            # Scroll down to load more results
            scrolls = 0
            while scrolls < 10:  # Scroll about 10 times
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(random.uniform(0.5, 2))  # Add a random delay
                scrolls += 1

        # Scroll to load initial results
        # scroll_to_bottom()

        emails = set()  # Use a set to avoid duplicates
        
        # get body html
        body = driver.find_element_by_tag_name("body").text
        import pdb; pdb.set_trace()
        parsed_html = remove_html_tags(body)
      
        emails = extract_emails(parsed_html)


        # Cl    ose the browser
        driver.close()
        driver.quit()
        


        # Return the list of extracted emails
        return emails

    except Exception as e:
        # Ensure the browser is closed in case of an exception
        driver.quit()
        return
    
    
    
    
    


def get_google_search_results():
    # Define the base Google search URL
    query = '+"ceo" AND "%40gmail.com" -intitle:"profiles" -inurl:"dir/ " site:www.linkedin.com/in/ OR site:www.linkedin.com/pub/'
    page_number = 2 
    base_url = "https://www.google.com/search"
    
    # Calculate the 'start' parameter for the desired page
    results_per_page = 10  # Number of results per page
    start = (page_number - 1) * results_per_page
    
    # Define the query parameters
    params = {
        "q": query,     # Your search query
        "start": start  # Start index for results on the page
    }
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    # Send a GET request to Google
    response = requests.get(base_url, params=params, headers=HEADERS)
    import pdb; pdb.set_trace()
    if response.status_code == 200:
        return response.text
    else:
        print("Error:", response.status_code)
        return None

# Usage example to get the second page of results for the provided query
 # Change this to the desired page number
 

 
