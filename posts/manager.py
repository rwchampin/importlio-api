from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from ai.assistant import Assistant as AssistantAI

posts = [
    'https://www.autods.com/blog/dropshipping-tips-strategies/selling-online',
    'https://www.autods.com/blog/suppliers-marketplaces/furniture-dropshipping-suppliers',
    'https://www.autods.com/blog/dropshipping-tips-strategies/best-dropshipping-websites',
    'https://www.autods.com/blog/product-finding/best-winter-products-to-dropship',
    'https://www.autods.com/blog/suppliers-marketplaces/dropshipping-suppliers-georgia',
    'https://www.autods.com/blog/product-finding/december-23-best-dropshipping-products',
    'https://www.autods.com/blog/suppliers-marketplaces/chinese-suppliers',
    'https://www.autods.com/blog/suppliers-marketplaces/dropshipping-suppliers-california',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropship-from-aliexpress-to-amazon',
    'https://www.autods.com/blog/suppliers-marketplaces/temu-dropshipping',
    'https://www.autods.com/blog/product-finding/amazon-best-selling-niches',
    'https://www.autods.com/blog/dropshipping-tips-strategies/wholesale-suppliers',
    'https://www.autods.com/blog/product-finding/dropship-auto-parts',
    'https://www.autods.com/blog/dropshipping-tips-strategies/supplement-dropshipping',
    'https://www.autods.com/blog/product-finding/november-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/google-trends-dropshipping',
    'https://www.autods.com/blog/dropshipping-tips-strategies/jewelry-dropshipping-etsy',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropshipping-challenges',
    'https://www.autods.com/blog/product-finding/best-selling-item-on-facebook-marketplace',
    'https://www.autods.com/blog/product-finding/dropshipping-drones',
    'https://www.autods.com/blog/success-stories/general-online-store',
    'https://www.autods.com/blog/product-finding/shopify-niches',
    'https://www.autods.com/blog/suppliers-marketplaces/etsy-dropshipping-suppliers',
    'https://www.autods.com/blog/product-finding/october-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/ebay-vs-shopify-dropshipping',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropship-on-amazon-without-money',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropshipping-api',
    'https://www.autods.com/blog/dropshipping-tips-strategies/ecommerce-business-examples',
    'https://www.autods.com/blog/dropshipping-tips-strategies/product-landing-page-examples',
    'https://www.autods.com/blog/suppliers-marketplaces/woocommerce-vs-shopify-dropshipping',
    'https://www.autods.com/blog/dropshipping-tips-strategies/instagram-dropshipping',
    'https://www.autods.com/blog/product-finding/best-things-to-sell-on-amazon',
    'https://www.autods.com/blog/product-finding/september-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/amazon-product-research',
    'https://www.autods.com/blog/marketing/dropshipping-ads',
    'https://www.autods.com/blog/dropshipping-tips-strategies/tiktok-ad-spy',
    'https://www.autods.com/blog/dropshipping-tips-strategies/best-amazon-dropshipping-courses',
    'https://www.autods.com/blog/dropshipping-tips-strategies/start-dropshipping-with-no-money',
    'https://www.autods.com/blog/product-finding/gaming-dropshipping',
    'https://www.autods.com/blog/dropshipping-tips-strategies/start-dropshipping-cost',
    'https://www.autods.com/blog/suppliers-marketplaces/shein-dropshipping',
    'https://www.autods.com/blog/product-finding/august-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropshipping-to-ebay',
    'https://www.autods.com/blog/dropshipping-tips-strategies/amazon-dropshipping-uk',
    'https://www.autods.com/blog/dropshipping-tips-strategies/wordpress-dropshipping',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropshipping-profit-margin',
    'https://www.autods.com/blog/product-finding/amazon-trends',
    'https://www.autods.com/blog/suppliers-marketplaces/luxury-dropshipping-suppliers',
    'https://www.autods.com/blog/dropshipping-tips-strategies/amazon-dropshipping-software',
    'https://www.autods.com/blog/product-finding/dropship-baby-products-uk',
    'https://www.autods.com/blog/product-finding/july-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/dropshipping-automation',
    'https://www.autods.com/blog/suppliers-marketplaces/tshirt-dropshipping-uk',
    'https://www.autods.com/blog/dropshipping-tips-strategies/shopify-dropship-review',
    'https://www.autods.com/blog/suppliers-marketplaces/fast-dropshipping-suppliers',
    'https://www.autods.com/blog/dropshipping-tips-strategies/sell-on-amazon-without-inventory',
    'https://www.autods.com/blog/product-finding/june-23-best-dropshipping-products',
    'https://www.autods.com/blog/dropshipping-tips-strategies/how-to-sell-on-shopify',
    'https://www.autods.com/blog/dropshipping-tips-strategies/hybrid-dropshipping',
    'https://www.autods.com/blog/suppliers-marketplaces/amazon-dropshipping-suppliers',

]
class Manager:
    def __init__(self):
        self.source = 'https://www.autods.com/blog/'
             
    def write_posts(self):
        ass = AssistantAI()
        # loop ofer ever line of the file post_sources.txt
        for line in posts:

            # await async fn
            
            ass.rephrase(line)
            
            # create a BeautifulSoup object
            
            # get the 2