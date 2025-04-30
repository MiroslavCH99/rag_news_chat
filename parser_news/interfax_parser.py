import re
import time
import datetime

import requests
import pandas as pd
import numpy as np

from tqdm import tqdm
from bs4 import BeautifulSoup


def get_page(p) -> list:
    """A function to retrieve data from a web page."""

    # Generating the url for the request
    url = f'https://www.interfax.ru/news/{p}'

    # Receiving a response from the server
    response = requests.get(url)

    # Convert the response to a BeautifulSoup object
    tree = BeautifulSoup(response.content, 'html.parser')

    # Find all the news for the day
    news = tree.find_all('div', {'data-id': re.compile('\d+')})

    info = []

    # Going around every news item
    for post in news:
        time = post.find('span')
        if time:
            time = time.text
        else:
            time = "?"

        title = post.h3.get_text()
        if title:
            title = title
        else:
            title = "?"

        link = post.a['href']
        id = link.split('/')[-1]

        if "https://www.interfax.ru/" in link:
            urli = link
        else:
            urli = 'https://www.interfax.ru' + link

        # Going inside each news item we found
        try:
            response_inner = requests.get(urli)
        except:
            continue
        tree_inner = BeautifulSoup(response_inner.content, 'html.parser')

        # If this is news from fontanka.ru
        if "https://www.interfax.ru/" in urli:
            topic = tree_inner.find('aside', {'class': 'textML'}).a.get_text()
            contents = ''
            content = tree_inner.find('article', {'itemprop': 'articleBody'}).find_all('p')
            for x in content:
                contents = contents + x.get_text() + ' '
            content = contents.strip()
            content = re.sub('.* INTERFAX.RU - ', '', content)

        else:
            content = "?"
            topic = "?"

        row = {
            'id': id,
            'date': p,
            'title': title,
            'topic': topic,
            'url': urli,
            'time': time,
            'content': content
        }

        info.append(row)

    return info

if __name__ == "__main__":
    def get_frame_news_year(start_year:int, end_year:int):
        infa = []
        for yy in tqdm(range(end_year, start_year, -1)):
            for mm in tqdm(range(12, 0, -1)):
                for dd in tqdm(range(31, 0, -1)):
                    p = f'{yy:04}/{mm:02}/{dd:02}'
                    try:
                        infa.extend(get_page(p))
                        df = pd.DataFrame(infa)
                        infa = []

                    except Exception as e:
                        print(f"Failed to get data for: {p}. Exception: {e}")
                        pass
        df = df[(df['topic']!='topic')]

        return df