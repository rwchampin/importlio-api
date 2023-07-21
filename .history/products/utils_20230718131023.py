import random
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def get_random_device():
    devices = ["iPhone 11", "Pixel 2", "iPad Mini"]
    return random.choice(devices)


def get_random_browser():
    browsers = ["chromium", "firefox", "webkit"]
    return random.choice(browsers)


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    ]
    return random.choice(user_agents)


BROWSERS = ["chromium", "firefox", "webkit"]


def get_page_html(url):
    with sync_playwright() as playwright:
        browser_type = random.choice(BROWSERS)
        browser = getattr(playwright, browser_type).launch()
        context = browser.new_context(user_agent=select_random_user_agent())
        page = context.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
        return html


def select_random_device():
    with sync_playwright() as playwright:
        devices = playwright.devices
        if devices:
            return random.choice(devices).name
    return None


def select_random_user_agent():
    with sync_playwright() as playwright:
        devices = playwright.devices
        if devices:
            device = random.choice(devices)
            return device["userAgent"]
    return None


# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

	except AttributeError:
		price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = ""	

	return available