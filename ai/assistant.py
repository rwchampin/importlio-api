from openai import OpenAI
import tiktoken, requests, json
from .models import Assistant, ChatRoom, AssistantModel
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from .split_string import split_string_with_limit
# from .models import Post, Tag, Category, PostType, PostTopicIdeas, PostOutline, PostOutlineItem, PostRephrase, PostRephraseItem

# class for openai manager that handles the init, and custom functions
from bs4 import BeautifulSoup

system_messages = {
    'title': 'The title should have 2 or more seo keywords in it and the first word must be one of the keywords.  Try to keep this title under 60 characters.',
    'subtitle': 'The subtitle should have 2 or more seo keywords in it and the first word must be one of the keywords.  Try to keep this subtitle under 60 characters.',
    'excerpt': 'The excerpt should have 2 or more seo keywords in it and the first word must be one of the keywords.  Try to keep this excerpt under 60 characters.',
    'REPHRASE': 'You will parse large strings of html and rewrite/rephrase the inner text of the html so that it is totally unique.  you will return a totally rewritten string containing the same html, and NEW unique inner text of the html.  You will rewrite the inner text while keeping the same overall concept of the initial topic.   You will return me a new string containing the html tags and the newly written inner text.  For example you will be given a string such as: `<section><h2>How to make a website</h2><p>First you need to learn HTML, CSS, and Javascript.</p></section>` and you will return a new string such as: `<section><h2>Building Websites: A comprehensive guide</h2><p>Building websites requires three primary skillsets.  They are HTML,CSS & javascript.</p></section>`.  The strings of html i provide you will often be more complex, with nested html structures that will require you to use your best judgement of the overall topic.',
    'basic_assistant': 'You are a helpful assistant that helps me by answering my questions.',
}
company_info = 'You are a helpful assistant for a Shopify dropshipping product importer and manager app. Keep the company in mind when answering questions.'
class AssistantManager:
    # init function
    def __init__(self):
        self.client = OpenAI()
        self.model_options = self.client.models.list()
        self.assistant = Assistant()

    # function to get the model options
    def get_model_options(self):
        print(self.model_options)
        return self.model_options
    
    # return assistants
    def get_assistants(self):
        return Assistant.objects.all()
     


class Assistant:
    # init function
    def __init__(self, model_type='gpt-3.5-turbo'):
        self.client = OpenAI()
        self.system_message = system_messages['REPHRASE']
        self.model = AssistantModel.objects.get(name=model_type)
        self.messages = self.set_system_message()

        self.token_encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
        self.max_tokens = 2000
    # function to set the model
    
    def set_system_message(self):
        m = {}
        m['role'] = 'system'
        m['content'] = self.system_message
    
    def add_user_message(self, message):
        m = {}
        m['role'] = 'user'
        m['content'] = message
        self.messages.append(m)
        
    def add_assistant_message(self, message):
        m = {}
        m['role'] = 'assistant'
        m['content'] = message
        self.messages.append(m)
    
    def create_message(self, role, content):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        import pdb; pdb.set_trace()
        return response.choices[0].text
    
    def get_info(self):
        for m in self.client.models.list():
            print(m)

    def set_system_message(self, type='REPHRASE', message=None):
        if message:
            self.system_message = message
        else:
            self.system_message = system_messages[type] 
            
    def set_model(self, model):
        self.model = AssistantModel.objects.get(name=model)
        self.set_token_encoding()

    def set_token_encoding(self):
        self.token_encoding = tiktoken.encoding_for_model(self.model.name)
        
    def get_token_count(self, text):
        return len(self.token_encoding.encode(text))
    
    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens
        
    def valid_text_size(self, text):
        c = self.get_token_count(text)
        if (c*2) > self.max_tokens:
            return False
        return True
    
    def create_title(self, data):
        print('create title')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": company_info +"You will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me a blog title with seo best practices for a shopify dropshipping app in mind.  You must use 1 seo keyword as the first word in the title and at least 1 additional keyword in the title. The title must be under 60 characters long. You will return a json object containing the title. The json object will look like: {title: 'my title'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        print(json.loads(res)['title'])
        return json.loads(res)['title']
    
    def create_subtitle(self, data):
        print('create subtitle')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": company_info + "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an blog subtitle with seo best practices in mind.  You must use 3-6 seo keywords in the subtitle. The subtitle must be under 60 characters long. You will return a json object containing the subtitle. The json object will look like: {subtitle: 'my subtitle'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['subtitle']
    
    def create_excerpt(self, data):
        print('create excerpt')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": company_info + "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an blog excerpt with seo best practices in mind.  You must use 3-10 seo keywords in the excerpt. The excerpt must be under 120 characters long. You will return a json object containing the excerpt. The json object will look like: {excerpt: 'my excerpt'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['excerpt']
    
    def create_headline(self, data):
        print('create headline')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": company_info + "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an blog headline with seo best practices in mind.  The headline must be under 5 words long. The headline is a small title that goes above the main title, as kind of an intro to the title. You will return a json object containing the headline. The json object will look like: {headline: 'my headline'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['headline']
    
    def create_shadowText(self, data):
        print('create shadowText')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content":company_info +  "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an blog shadowText title with seo best practices in mind.  The shadowText must be under 5 words long. The shadowText is a small title the is mainly for visual effect and is rotated sideways and positioned fixed on the left of the screen with an opaque effect but still has seo ranking possibilty.  The shadowtext title should have at least 1 seo keyword and be 3-5 words long. You will return a json object containing the shadowText. The json object will look like: {shadowText: 'my shadowText'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['shadowText']
    
    def create_seo_title(self, data):
        print('create seo_title')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content":company_info +  "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an seo title with seo best practices in mind.  The seo title must be under 60 characters long. You will return a json object containing the seo_title. The json object will look like: {seo_title: 'my seo_title'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['seo_title']
    
    def create_seo_description(self, data):
        print('create seo_description')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content":company_info +  "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an seo description with seo best practices in mind.  The seo description must be under 160 characters long. You will return a json object containing the seo_description. The json object will look like: {seo_description: 'my seo_description'}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content": t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['seo_description']
    
    def create_seo_keywords(self, data):
        print('create seo_keywords')
        t = json.dumps(data)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": company_info + "You are a helpful assistant who will recieve a json object containing a json object containing seo keywords and summaries about a blog post.  Write me an seo keywords with seo best practices in mind.  The seo keywords must be a csv list of 20-50 words or phrases for the meta keywords tag. You will return a json object containing the seo_keywords. The json object will look like: {seo_keywords: ['keyword1', 'keyword2', 'keyword3']}.  You will use the data I provide to calculate the best possible single answer for each." },
                {"role": "user", "content":  t}
            ]
        )

        res = response.choices[0].message.content
        
        return json.loads(res)['seo_keywords']
    
    def create_details(self, soup):
        title = soup.title.string
         # if description is present, get its inner text
        x = soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
        
        post_content = soup.find('div', attrs={'class': 'post-content'})
        text = post_content.get_text()

        # split the text into chunks of 5000 characters
        data = {}
        data['seo_keywords'] = []
        data['summaries'] = []
        chunks = split_string_with_limit(text, self.max_tokens/2, self.token_encoding)

        for chunk in chunks:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": company_info + " you will recieve a chunk of text for a long blog post. Analyze the text and identify as many seo keywords or topics we can use to rank better on google for words and phrases that will benefit a shopify dropshipping app company.  You will also return an extensive summary of everyhing mentioned in the text to help us make additional data about the post.  You will return a json object containing the seo_keywords and summaries. The json object will look like: {seo_keywords: ['keyword1', 'keyword2', 'keyword3'], summaries: ['summary1', 'summary2', 'summary3']}.  You will use the data I provide to calculate the best possible single answer for each." }, 

                    {"role": "user", "content": str(chunk)}
                ]
            )
            res = response.choices[0].message.content
            res = json.loads(res)
            data['seo_keywords'] = data['seo_keywords'] + res['seo_keywords']
            data['summaries'] = data['summaries'] + res['summaries']
        # split the chunks into chunks of 5000 tokens
         

        
        post = {}
        post['title'] = self.create_title(data)
        post['subtitle'] = self.create_subtitle(data)
        post['excerpt'] = self.create_excerpt(data)
        post['headline'] = self.create_headline(data)
        post['shadowText'] = self.create_shadowText(data)
        post['seo_title'] = self.create_seo_title(data)
        post['seo_description'] = self.create_seo_description(data)
        post['seo_keywords'] = self.create_seo_keywords(data)
        
        
        return post
    
    def rephrase(self, url):
        print('rephrase')
        data = {}
        html = requests.get(url)

        #make soup
        soup = BeautifulSoup(html.text, 'html.parser')

        # get class name post-content
        post_content = soup.find('div', attrs={'class': 'post-content'})
        
        # remove new lines
        print('create info')
        post= self.create_details(soup)
        # create post info


        post['featured_image'] = self.create_featured_image(post)
        
        

        print('rephrase body')
        chunks = self.prepare_html(str(post_content))

        count = 0
        responses = ''
        for chunk in chunks:
            response = self.client.chat.completions.create(
                model=self.model.name,
                messages=[
                    {
                        'role': 'system',
                        'content': self.system_message
                    },{
                        'role': 'user',
                        'content': str(chunk)
                    }
                ]
            )
            m = response.choices[0].message.content
            print(m)
            print(count)
            count += 1
            responses += m
            

        # write the post
        post['content'] = responses

        return post
    
    def removeAttrs(self, soup):
        for tag in soup.find_all(True):
            tag.attrs = None
        return soup
        
    def prepare_html(self, html):
         # remove all new lines
        html = html.replace('\n', '')
        
        # create beautilful soup object
        soup = BeautifulSoup(html, 'html.parser')

        # remove all html attrs
        soup = self.removeAttrs(soup)
            
        # remove all new lines
        [s.extract() for s in soup('br')]
        # remove all script tags
        [s.extract() for s in soup('script')]
        
        # remove all style tags
        [s.extract() for s in soup('style')]
        
        # remove all meta tags
        [s.extract() for s in soup('meta')]
        
        # remove all image tags
        [s.extract() for s in soup('img')]
        
        # remove all video tags
        [s.extract() for s in soup('video')]

        # get the first child
        parent = soup.contents[0]
        children = parent.contents
        newlist = []
         # loop over children and print the length
        for child in children:
            # convert child to string
            child_string = str(child)
            if self.valid_text_size(child_string):
                # remove the child from the parent
                newlist.append(child)
        print(len(newlist))
        return newlist
    
    
    def create_info(self, soup):
        print('create info')
         # get title and description
        title = soup.title.string
        
        # if description is present, get its inner text
        x = soup.select('meta[name="description"]')
        # if x is not empty, get the content
        if x:
            description = x[0].attrs["content"]
            
        # get 
        s = {
            'title': title,
            'description': description,
        }

        # stringify info
        s = json.dumps(s)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant who will recieve a title & a description, if they are present for a blog post.  you will use the title & description to create a unique title, subtitle,excerpt, headline - which is a 2-5 word small intro title above the title, a shadowText - which is a 3-5 word alternative title used for visual design on the page and must be related to the post title, a post excerpt. You will also create a seo_title, seo_description. If the word 'AutoDS' is present, replace it with 'Importlio'. You will return a json object containing the title, subtitle,excerpt, headline, shadowText, seo_title, seo_description. The json object will look like: {title: 'my title', excerpt: 'some excerpt', subtitle: 'my subtitle', headline: 'my headline', shadowText: 'my shadowText', seo_title: 'my seo_title', seo_description: 'my seo_description'}"},
                {"role": "user", "content": s}
            ]
        )

        tojson = response.choices[0].message.content
        
        # convert to json

        tojson = json.loads(tojson)
        return tojson
    
    def create_featured_image(self, post):
        print('create featured image')
        title = post['title']
        subtitle = post['subtitle']
        excerpt = post['excerpt']
        keywords = post['seo_keywords']
        # Define your prompt for DALL·E
        prompt = 'My company is a Dropshipping product importer and management app for Shopify stores.  I have a blog post that needs a beautiful eye catching featured image.  The blog post is based on the following details.  The title: ' + title + ' and the subtitle: ' + subtitle + ' and the excerpt: ' + excerpt + ' and the seo keywords: ' + str(keywords) + '.  Please create a beautiful featured image for this blog post that makes sense for a post with the previously mentioned info.  The image should be landscape, hi-res, unique & eye catching.  The image should be 1920px1080px.  The image should be a png file.  The image should be under 1mb.  The image should be unique and not used anywhere else on the internet.  The image should be related to the topic of the blog post.  The image should be a beautiful image that will make people want to read the blog post.  The image should be a beautiful image that will make people want to read the blog post.  The image should use gradients & colors to make it stand out.'
        
        

        # Call the OpenAI API to generate the image
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            n=1  # Specify the number of images to generate
        )

        img_url = response.data[0].url

        # Download the image using requests
        image_response = requests.get(img_url)
        
        return image_response.content
    
    
    def write_post(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # title tag
        title = soup.title.string
        
        # meta description tag
        description = soup.find('meta', attrs={'name': 'description'})
        import pdb; pdb.set_trace()
        p = 'this is the title: ' + title + ' and this is the description: ' + description['content']
        t = self.create_title(p)
        import pdb; pdb.set_trace()
        
 
         
         