import requests
from bs4 import BeautifulSoup

def extract_info(url):
    # Download the webpage
    response = requests.get(url)
    # Check to make sure the download was successful
    if response.status_code != 200:
        print(f"Failed to download page: {url}, status code: {response.status_code}")
        return [], [],

    # Parse the downloaded page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main tag and class
    content_wrapper = soup.find('main', class_='content-wrapper')

    # Check if it exists
    if content_wrapper is None:
        print(f"Couldn't find main tag with class 'content-wrapper', for page {url}")
        return [],[]

    # Find the div with class 'container flex'
    container_flexe = content_wrapper.find('div', class_='container flexe')

    # Check if it exists
    if container_flexe is None:
        print(f"Couldn't find div with class 'container flexe', page: {url}")
        return [],[]

    # Find the div with class 'oscont'
    oscont = container_flexe.find('div', class_='oscont')

    # Check if it exists
    if oscont is None:
        print(f"Couldn't find div with class 'oscont' , page: {url}")
        return [],[]
        
    # Extract alt text from images
    alt_texts = [img['alt'] for img in oscont.find_all('img') if 'alt' in img.attrs]

    # Extract text from divs with class 'sttext'
    div_texts = [div.get_text(strip=True) for div in oscont.find_all('div', class_='sttext')]

    return alt_texts, div_texts

# Using the function
# url = "https://poemata.ru/poets/dzhalil-musa/dorogi/" # replace with your actual URL
# alt_texts, div_texts = extract_info(url)
# print("Alt texts:", alt_texts)
# print("Div texts:", div_texts)
