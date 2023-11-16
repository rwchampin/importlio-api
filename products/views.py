from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ScrapeURLSerializer, ProductSerializer
import requests, random, time
from bs4 import BeautifulSoup, Comment
from .utils import extract_product_info
from rest_framework.decorators import api_view
from utils.scraping.get_proxy import get_proxy
from selectorlib import Extractor

from .proxy import ProxyManager
import os, re
import openai

proxy_manager = ProxyManager()

username = "geonode_ULZNrg2KXZ"
password = "3c404204-1d3e-4bb0-b47e-f863d6ec9deb"
GEONODE_DNS = "rotating-residential.geonode.com:9000"
 

# Create an Extractor by reading from the YAML file
# e = Extractor.from_yaml_file('selectors.yml')

# from .utils import get_title, get_description, get_price, get_reviews, get_images, get_availability, get_variants
class ScrapeAmazonViewSet(viewsets.ViewSet):
    http_method_names = ['post']
    authentication_classes = []
    permission_classes = []
    
    def create(self, request):
        headers = ({'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'})
        response = requests.get('https://www.amazon.com/s?k=laptops&crid=1BKE05LZEL0B2&sprefix=laptops%2Caps%2C87&ref=nb_sb_noss_1', headers=headers)
        import pdb; pdb.set_trace()
        if response.status_code == 200:
            product_list = extract_product_info(response.content)
            import pdb; pdb.set_trace()
            # soup = BeautifulSoup(response.content, "lxml")
            # title = get_title(soup)
            # description = get_description(soup)
            # price = get_price(soup)
            # reviews = get_reviews(soup)
            # images = get_images(soup)
            return Response(product_list, status=status.HTTP_200_OK)
            # Save to database
            # product = Product.objects.create(
            #     url=url,
            #     title=title,
            #     description=description,
            #     price=price,
            #     reviews=reviews,
            #     images=images,
            #     availability=availability,
            #     variants=variants
            # )
            # product_serializer = ProductSerializer(product)
            # return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to retrieve the page.'}, status=status.HTTP_400_BAD_REQUEST)



# fn that loops over all div and finds the ones with the most classes 




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    


def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    # print("Proxy used:", proxy)
    proxy = {"http":"http://{}:{}@{}".format(username, password, GEONODE_DNS)}
    import pdb; pdb.set_trace()
    r = requests.get(url, headers=headers, proxies=proxy)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    
    return r.content

@api_view(['POST'])
def get_data(request):      
    # Create an Extractor by reading from the YAML file
    path_to_yaml = os.path.join(os.path.dirname(__file__), 'search_results.yml')
    e = Extractor.from_yaml_file(path_to_yaml)
    html = []
    # get the url from the request
    # url = 'https://www.amazon.com/s?k=new-releases/baby-products'
    run = True
    num = 100
    start = 0
    
    while run and start < 300:
        url = f'https://www.google.com/search?num=100&start={start}&q=+"shopify" AND "%40gmail.com" -intitle:"profiles" -inurl:"dir/+"+site:www.linkedin.com/in/+OR+site:www.linkedin.com/pub/'
        # get the html from the url
        res = scrape(url)
        
        if res is None:
            run = False
        else:
            emails = extract_email_addresses(res)
            html = html + emails
            # increment the start by 100
            start += 100
            # pause random time between 5 and 10 seconds
            time.sleep(random.randint(1, 2))
    # get text from the html
    
    saveEmails(html)
    # get data from the html
    # data = e.extract(html.text)
    
    return Response(html, status=status.HTTP_200_OK)
        

def saveEmails(emails):
    for email in emails:
        try:
            Product.objects.create(email=email)
        except:
            pass
        
# fn to return email addresses from a string
def extract_email_addresses(html_content):
    email_addresses = set()  # Using a set to avoid duplicates
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    # loop over the html content

    # Use regular expressions to find email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
    email_regex = re.compile(email_pattern)

    # Find all text in the HTML, including text within <em> tags
    text = ''.join(soup.stripped_strings)

    # Search for email addresses and add them to the set
    for match in email_regex.finditer(text):
        email_addresses.add(match.group())

    return list(email_addresses)
        
        # "<!doctype html><html itemscope=\"\" itemtype=\"http://schema.
        
        
        
        
        
        
        
        
# def old:
#     # remove all comments from the HTML
#     comments = body.findAll(text=lambda text:isinstance(text, Comment))
#     [comment.extract() for comment in comments]
    
#     # remove all <script> tags, <noscript> tags, and <style> tags
#     for script_tag in body.find_all('script'):
#         script_tag.extract()
        
#     for noscript_tag in body.find_all('noscript'):
#         noscript_tag.extract()
        
#     for style_tag in body.find_all('style'):
#         style_tag.extract()
        
#     # remove all html elements with the word 'nav' in the id or class attribute
#     nav_elements = body.find_all(lambda tag: any('nav' in attr for attr in tag.attrs))
#     for nav_element in nav_elements:
#         nav_element.extract()
        
#     openai.api_key = "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"
#     instructions = 'I am going to send you multiple HTML strings to parse.  I will tell you when i am done.  You will say `received, waiting for more.` to acknowledge you have received. you will not do anything but receive data until i say `i am done`.  you will then ask me for instructions as to what you need to do to the data given when i am done sending. are you ready?'
    
#     # add the instructions to the messages list
#     messages.append({'role': 'user', 'content': instructions})
#     # send instructions to ai
#     chat_completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#     )

#     # add the response to the messages list
#     messages.append({'role': 'assistant', 'content': chat_completion.choices[0].message.content})
#     #send the remaining string to the AI to parse
#     # split the msg up into 4000 character chunks

#     body = body.text.split()
#     msg_chunks = []
#     msg_chunk = ''
#     for word in body:
#         if len(msg_chunk) < 4000:
#             msg_chunk = msg_chunk + ' ' + word
#         else:
#             msg_chunks.append(msg_chunk)
#             msg_chunk = ''
#     msg_chunks.append(msg_chunk)
    
#     for msg_chunk in msg_chunks:
#         # send the msg chunk to the AI and add to the messages list
#         messages.append({'role': 'user', 'content': msg_chunk})
#         chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#         messages.append({'role': 'assistant', 'content': chat_completion.choices[0].message.content})
#         print(messages)
#     # send the final instructions to the AI
#     instructions = 'I am done sending you the HTML strings. The HTML given is of a ecommerce product page. You will parse the html I gave you in the previous messages.  Please parse the HTML I have previously provided and return to me an array of objects that represent each product you find. Each product should have a title, price, rating, review count, a list of urls for the pictures related to each product, and any other information you see fit.  Please return the array of objects as a JSON string.'
#     # add the instructions to the messages list
#     messages.append({'role': 'user', 'content': instructions})
#     chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#     messages.append({'role': 'assistant', 'content': chat_completion.choices[0].message.content})
    
#     # send the final instructions to the AI
#     instructions = 'yes please send me the parsed product data in json format'
#     # add the instructions to the messages list
#     messages.append({'role': 'user', 'content': instructions})
#     chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
#     messages.append({'role': 'assistant', 'content': chat_completion.choices[0].message.content})
#     print(messages)
#     print(chat_completion.choices[0].message.content)
#     return Response({'data': messages}, status=status.HTTP_200_OK)