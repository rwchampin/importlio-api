import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from proxies.models import Proxy

from .utils import (
    get_title,
    get_price,
    get_rating,
    get_reviews_count,
    get_availability,
    get_headers,
)
import requests

from bs4 import BeautifulSoup
import requests, random

class ProductViewSet(ViewSet):
	authentication_classes = []
	permission_classes = []

	def get_random_proxy():
		proxies = Proxy.objects.all()  # Assuming you are using Django ORM and have a Proxy model

		if not proxies:
			raise Exception("No proxies found.")

		random_proxy = random.choice(proxies)
		return random_proxy

	def get_html(url):
		proxies = Proxy.objects.all()
		random_proxy = random.choice(proxies) if proxies else None
		headers = get_headers(url)
    
		try:
			r = requests.get(url, headers=headers, proxies=random_proxy)
			r.raise_for_status()  # Raise an exception if the request was unsuccessful
			return r.text
		except requests.RequestException as e:
			print(f"Error during request: {e}")
			return None
    
    def scrape_product(url):
        html = get_html(url)

	@action(detail=False, methods=["get"])
	def scrape_product_page(self, request):
		product_url = request.query_params.get("url")
		if not product_url:
			return Response({"error": "Product URL is required."}, status=400)

		product = scrape_product(product_url)


           

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
