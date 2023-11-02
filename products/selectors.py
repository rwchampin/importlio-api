def remove_head_script_noscript_style_tags(soup, html_string):
    # Create a BeautifulSoup object to parse the HTML

    # remove all comments from the HTML
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    
    #remove all html elements with the word 'nav' in the id or class attribute
    nav_elements = soup.find_all(lambda tag: any('nav' in attr for attr in tag.attrs))
    for nav_element in nav_elements:
        nav_element.extract()
        

    # remove the header tag and its contents
    header_tag = soup.find('header')
    if header_tag:
        header_tag.extract()
    # Remove the <head> tag and its contents
    head_tag = soup.head
    if head_tag:
        head_tag.extract()

    # Remove all <script> tags
    for script_tag in soup.find_all('script'):
        script_tag.extract()

    # Remove all <noscript> tags
    for noscript_tag in soup.find_all('noscript'):
        noscript_tag.extract()

    # Remove all <style> tags
    for style_tag in soup.find_all('style'):
        style_tag.extract()

    # Return the modified HTML without the specified tags
    return str(soup)

def find_products(soup, substring):
    try:
        # Find all elements with attributes containing the specified substring
        elements = soup.find_all(lambda tag: any(substring in attr for attr in tag.attrs))
        
        # Return the elements
        return elements
    except:
        return None
