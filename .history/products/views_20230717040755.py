import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class ProductViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["get"])
    def parse_amazon_category(self, request):
        category_url = request.query_params.get(
            "url"
        )  # Get the category URL from the request parameters
        if not category_url:
            return Response({"error": "Category URL is required."}, status=400)

        async def scrape_amazon_category(url):
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()

                await page.goto(url)
                html = await page.content()

                await browser.close()

                return html

        async def main():
            html = await scrape_amazon_category(category_url)
            soup = BeautifulSoup(html, "html.parser")
            # Perform parsing operations using BeautifulSoup

            # Extract the desired information from the parsed HTML

            # Return the extracted data
            data = {
                "result": "Parsing successful"
            }  # Replace with the actual extracted data

            return Response(data)

        asyncio.run(main())
