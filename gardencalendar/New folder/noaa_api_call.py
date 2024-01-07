"""THIS MODULE--
scrapes the website https://www.almanac.com/gardening/frostdates/zipcode/{xyzabc}

and retrieves frost information. This will be used to populate the user's garden info.

"""

import requests

from bs4 import BeautifulSoup

from time import sleep

import random


frost_info=[]


def scrape(url):

    user_agents = [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",

        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",

        "Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",

        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",

        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",

        "Mozilla/5.0 (Linux; Android 10; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",

    ]

    # I am randomly selecting user agents to prevent bot detection
    headers = {"User-Agent": random.choice(user_agents)}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        return response.text

    else:

        print(f"Shiiiit! I messed up man. I messed up. I messed up. I messssssseeeeedddddddddd uppppppp: {response.status_code}")

        return None



def clean_data(html_content):
    
    """GETTING ALL td tags on the web page.
    """

    if html_content:

        soup = BeautifulSoup(html_content, 'html.parser')

        td_tags = soup.find_all('td')

        for td_tag in td_tags:
            for info in td_tag:
                frost_info.append(info)

    else:

        print("No HTML content to scrape.")



        
zipcode=input("enter a zipcode--->>")

url_to_scrape = f'https://www.almanac.com/gardening/frostdates/zipcode/{zipcode}'

html_content = scrape(url_to_scrape)



if html_content:

    clean_data(html_content)

    print(frost_info)
    print(f'your city state is..............  {frost_info[0]}')
    print(f'your elevation  is..............  {frost_info[1]} ft.')
    print(f'your last frost in spring is....  {frost_info[2]}')
    print(f'your first frost in fall is.....  {frost_info[3]}')
    print(f'you have {frost_info[4]} days to grow stuff.')






