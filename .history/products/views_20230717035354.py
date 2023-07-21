from django.shortcuts import render

# Create your views here.
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def scrape_amazon_category(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(url)
        html = await page.content()

        await browser.close()

        return html
