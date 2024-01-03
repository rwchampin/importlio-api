import os
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ai.assistant import Assistant as AssistantAI

class Manager:
    def __init__(self):
        self.source = 'https://www.autods.com/blog/'

    def write_posts(self):
        ass = AssistantAI()
        url_index = 0
        key_index = 13

        current_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(current_dir, 'autods.csv')

        # open the file
        with open(filename, 'r', encoding='utf-8-sig') as f:  # Specify encoding with utf-8-sig to handle BOM
            # read the file
            reader = csv.reader(f)
            
            # loop over each row
            for row in reader:
                # Remove BOM character from the URL
                url = row[0]
                keyy = row[12]
                # call the rephrase function
                ass.rephrase(url,keyy)
