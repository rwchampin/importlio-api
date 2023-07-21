import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from proxies.models import Proxy
from .utils import (
    get_page_html,
    select_random_device,
    select_random_user_agent,
    get_random_browser,
)
import requests

from bs4 import BeautifulSoup
import requests


def get_user_agent():
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }
    return HEADERS


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

    # The webpage URL
    # URL = "https://www.amazon.com/Sony-PlayStation-Pro-1TB-Console-4/dp/B07K14XKZH/"

    # HTTP Request
    # webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data


class ProductViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []
    
    def get_headers(self):
        # Headers for request
		HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})
        

    @action(detail=False, methods=["get"])
    def scrape_product_page(self, request):
        product_url = request.query_params.get("url")
        if not product_url:
            return Response({"error": "Product URL is required."}, status=400)

        async def scrape_product(url):
            HEADERS = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
                "Accept-Language": "en-US, en;q=0.5",
            }
            webpage = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "lxml")
            # Outer Tag Object
            title = soup.find("span", attrs={"id": "productTitle"})
            # Inner NavigableString Object
            title_value = title.string
            # async with async_playwright() as p:
            return title_value

            html = await scrape_product(product_url)
            soup = BeautifulSoup(html, "html.parser")
            # print(soup)
            # Perform parsing operations using BeautifulSoup

            # Extract the desired information from the parsed HTML

            # Return the extracted data
            data = {
                "result": "Parsing successful"
            }  # Replace with the actual extracted data

            return Response(data)

        asyncio.run(main())

        # @action(detail=False, methods=["post"])
        # def scrape_multiple_products(self, request):
        product_urls = request.data.get("urls")
        if not product_urls:
            return Response({"error": "Product URLs are required."}, status=400)

        # async def scrape_product(url):
        #     async with async_playwright() as p:
        #         browser = await p.chromium.launch()
        #         page = await browser.new_page()

        #         await page.goto(url)
        #         html = await page.content()

        #         await browser.close()

        #         return html

        # @action(detail=False, methods=["get"])
        # def scrape_results_page(self, request):
        results_url = request.query_params.get("url")
        if not results_url:
            return Response({"error": "Results URL is required."}, status=400)

        async def scrape_results(url):
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                await page.goto(url)
                html = await page.content()

                await browser.close()

                return html

        async def main():
            html = await scrape_results(results_url)
            soup = BeautifulSoup(html, "html.parser")
            # Perform parsing operations using BeautifulSoup

            # Extract the desired information from the parsed HTML

            # Return the extracted data
            data = {
                "result": "Parsing successful"
            }  # Replace with the actual extracted data

            return Response(data)

        asyncio.run(main())
