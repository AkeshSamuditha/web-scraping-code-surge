import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch HTML content from {url}: {e}")
        return None


def extract_menu_items(base_url):
    urls = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    main_menu = soup.find_all('nav')


    for menu in main_menu:
        main_items = menu.find_all('a')

        for main_item in main_items:
            main_url = main_item['href'] if 'href' in main_item.attrs else None
            if not main_url.startswith('http'):
                main_url = BASE_URL + main_url

            # Process sub-items
            sub_items = []
            sub_menu = main_item.find_next('ul')
            if sub_menu:
                sub_links = sub_menu.find_all('a')  # Sub-items
                for sub_link in sub_links:
                    sub_url = sub_link['href'] if 'href' in sub_link.attrs else None
                    if sub_url and not sub_url.startswith('http'):
                        URL = SITE_URL + sub_url
                        urls.append(URL)

    return list(set(urls))


def extract_urls(section):
    """
    Extracts and returns a list of URLs from the given HTML section.

    Args:
        section (bs4.element.Tag): A BeautifulSoup Tag object representing an HTML section.

    Returns:
        list: A list of URLs (strings) extracted from the 'href' attributes of 'a' tags within the section.
              If the section itself is an 'a' tag with an 'href' attribute, an empty list is returned.
    """
    urls = []
    if section.name == 'a' and section.has_attr('href'):
        return []
    for anchor in section.find_all('a', href=True):
        url = anchor['href'].strip()
        if not url.startswith('http'):
            url = CURR_URL + url
        urls.append(url)
    return urls

def extract_text(section, tags=['p', 'ul', 'ol']):
    """
    Extract text from specified tags inside a section while preserving order.
    Args:
        section (bs4.element.Tag): The BeautifulSoup tag object representing the section to extract text from.
        tags (list of str, optional): A list of tag names to extract text from. Defaults to ['p', 'ul', 'ol'].
    Returns:
        list of str: A list of strings containing the extracted text from the specified tags.
    """
    """Extract text from specified tags inside a section while preserving order."""
    content = []


    if section.name in tags:
        content.append(section.get_text(strip=True))
    else:
        # find all tags and scrap text
        for element in section.find_all(True):
            if element.name in tags:
                content.append(element.get_text(strip=True))  # Extract text and remove extra spaces
    
    return content

def extract_code(section):
    """
    Extracts code blocks from the given section.

    Args:
        section (bs4.element.Tag): A BeautifulSoup Tag object representing an HTML section.

    Returns:
        str: A string containing the extracted code blocks.
    """
    code_blocks = section.find_all(True, 'cm-line')
    code_lines = []  
    
    for code in code_blocks:
        line_text = ' '.join(span.text for span in code.find_all('span'))
        
        code_lines.append(line_text)
    if code_lines:     
        full_code = {
            'language': 'javascript',
            'code' :'\n'.join(code_lines)
            }
        return full_code
    return None

def extract_section(header):
    """
    Extracts content from HTML header sections (h1 to h3) recursively.
    Args:
        header (Tag): BeautifulSoup Tag object representing the header.
    Returns:
        dict: A dictionary containing the title, description, code samples, URLs, and subsections.
    """
    title = header.text.strip()
    subsections = []
    text = []
    codes = []
    urls = []
    
    level = int(header.name[1]) 
    
    for sibling in header.find_next_siblings():
        # Stop when another header of the same or higher level is encountered
        if sibling.name in ['h1', 'h2', 'h3'] and int(sibling.name[1]) <= level:
            break
        
        # If the sibling is a header, Recursively process it as a subsection
        if sibling.name in ['h1', 'h2', 'h3']:
            subsections.append(extract_section(sibling)) 
        else:
            # Otherwise, extract text and other relevant data
            text.extend(extract_text(sibling)) 
            urls.extend(extract_urls(sibling)) 
            code_section = extract_code(sibling)
            if code_section:
                codes.append(code_section)
    
    content = "\n".join(text)
    return {
        "title": title,
        "description": content,
        "code_sample": codes,
        "urls": urls,
        "subsections": subsections 
    }
    
def scrape_page(main_url):
    """
    Scrapes the given webpage URL and extracts the main title, summary, and sections.
    Args:
        main_url (str): The URL of the webpage to scrape.
    Returns:
        dict: A dictionary containing the page title, source, URL, and sections with summary and content.
    """
    global CURR_URL
    CURR_URL = main_url
    soup = fetch_html(main_url)
    if not soup:
        return {}

    main_title = soup.find('title').text.strip() if soup.find('title') else "Untitled Page"
    sections = []

    # get page summary before scraping for titles
    first_h2 = soup.find('h2')
    if first_h2:
        texts = []
        for sibling in first_h2.find_previous_siblings():
            if sibling.name in ['h1', 'h3', 'h4']: 
                break
            texts.extend(extract_text(sibling))
        texts.reverse() 
        content = "\n".join(texts)
    for h2 in soup.find_all('h2'):
        sections.append(extract_section(h2))

    return {
        "title": main_title,
        "source": "react",
        "url": main_url,
        "sections": {
            'summary': content, 
            'content': sections}
    }
   
def scrape_react():
    global SITE_URL
    global BASE_URL
    SITE_URL = 'https://react.dev'
    BASE_URL = "https://react.dev/learn"
    urls = extract_menu_items(BASE_URL)
    all_data = []
    
    for url in urls:
        page_data = scrape_page(url)
        if page_data:
            all_data.append(page_data)
    return all_data

    

    
