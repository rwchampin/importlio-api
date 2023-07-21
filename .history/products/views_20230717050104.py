import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .utils import (
    get_page_html,
    select_random_device,
    select_random_user_agent,
    get_random_browser,
)


class ProductViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["get"])
    def scrape_product_page(self, request):
        product_url = request.query_params.get("url")
        if not product_url:
            return Response({"error": "Product URL is required."}, status=400)

        async def scrape_product(url):
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(url)
                html = await page.content()
				 
     			import pdb; 
        		pdb.set_trace()
				
    			await browser.close()

                return html

        async def main():
            html = await scrape_product(product_url)
            soup = BeautifulSoup(html, "html.parser")
            # Perform parsing operations using BeautifulSoup

            # Extract the desired information from the parsed HTML

            # Return the extracted data
            data = {
                "result": "Parsing successful"
            }  # Replace with the actual extracted data

            return Response(data)

        asyncio.run(main())

    @action(detail=False, methods=["post"])
    def scrape_multiple_products(self, request):
        product_urls = request.data.get("urls")
        if not product_urls:
            return Response({"error": "Product URLs are required."}, status=400)

        async def scrape_product(url):
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                await page.goto(url)
                html = await page.content()

                await browser.close()

                return html

        async def main():
            results = []
            for url in product_urls:
                html = await scrape_product(url)
                soup = BeautifulSoup(html, "html.parser")
                # Perform parsing operations using BeautifulSoup

                # Extract the desired information from the parsed HTML

                # Append the extracted data to the results list
                result = {
                    "url": url,
                    "data": "...",
                }  # Replace with the actual extracted data
                results.append(result)

            return Response(results)

        asyncio.run(main())

    @action(detail=False, methods=["get"])
    def scrape_results_page(self, request):
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
