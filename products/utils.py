import random, requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.parse
from proxies.models import Proxy
from django.db.models import F
from django.utils import timezone

ua = UserAgent


def scrape_product(url):
    html = get_html(url)


def get_random_proxy():
    proxies = Proxy.objects.all()
    print(proxies)
    # if proxy is not None and proxy.exists():
    #     return random.choice(proxy)
    # else:
    #     raise Exception("No proxies found.")


def get_html(url):
    try:
        headers = get_headers(url)
        proxies = get_random_proxy()
        import pdb

        pdb.set_trace()
        r = requests.get(url, headers=headers, proxies=proxies)
        r.raise_for_status()  # Raise an exception if the request was unsuccessful
        print(r.text)
        return r.text
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None


def create_google_referrer_from_url(amazon_product_url):
    base_url = "https://www.google.com/search?"
    product_name = extract_product_name(amazon_product_url)
    query_params = {"q": product_name + " site:amazon.com"}
    referrer_url = base_url + urllib.parse.urlencode(query_params)
    return referrer_url


def extract_product_name(amazon_product_url):
    parsed_url = urllib.parse.urlparse(amazon_product_url)
    path_parts = parsed_url.path.split("/")
    product_name = path_parts[-1]
    return product_name


def get_headers(url):
    ua = UserAgent()
    accept_types = "text/html,application/xhtml+xml,application/xml;q=0.9"
    random_language = random.choice(["en-US", "en"])
    referrer = create_google_referrer_from_url(url)

    headers = {
        "User-Agent": ua.random,
        "Accept-Language": random_language,
        "Accept-Encoding": "gzip, deflate",
        "Accept": accept_types,
        "Referer": referrer,
    }

    return headers


# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": "productTitle"})

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
        price = soup.find("span", attrs={"id": "priceblock_ourprice"}).string.strip()

    except AttributeError:
        price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find(
            "i", attrs={"class": "a-icon a-icon-star a-star-4-5"}
        ).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={"class": "a-icon-alt"}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={"id": "acrCustomerReviewText"}
        ).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={"id": "availability"})
        available = available.find("span").string.strip()

    except AttributeError:
        available = ""

    return available


 

def extract_product_info(html):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find all HTML sections with the specified attributes
    product_sections = soup.find_all('div', {'data-asin': True, 'data-index': True, 'data-uuid': True, 'data-component-type': 's-search-result'})
    
    # Initialize an empty list to store product information
    product_info_list = []
    
    for section in product_sections:
        # Extract the title
        title_element = section.find('h2', class_='a-size-mini')
        title = title_element.text.strip() if title_element else None
        
        # Extract the price
        price_element = section.find('span', class_='a-offscreen')
        price = price_element.text.strip() if price_element else None
        
        # Extract the image URL
        image_element = section.find('img', {'data-image-latency': 's-product-image'})
        image_url = image_element.get('src') if image_element else None
        
        # Create a dictionary for the product information
        product_info = {
            'title': title,
            'price': price,
            'image_url': image_url
        }
        
        # Add the product information to the list
        product_info_list.append(product_info)
    
    return product_info_list
