# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
# from tabulate import tabulate
import urllib.parse


pd.set_option('display.width', None)
pd.set_option('display.max_columns', 500)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)



# response = requests.get(url)

# soup = BeautifulSoup(response.text, "html.parser")

# logger.info(soup.prettify())
#
# results = []
# for item in soup.select("h2.Type-h2.Type-h2--altFamily"):
#     title = item.text.strip()
#     results.append(title)
#
# print(results)

def get_articles(search_term):
    url = f"https://www.opic.com/upphandlingar/sverige/?q={search_term}&a=false"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select("h2.Type-h2.Type-h2--altFamily"):
        title = item.text.strip()
        results.append(title)

    # Find the section with class="Site-section"
    section = soup.find('section', {'class': 'Site-section'})

    # Find all the links in the section that have the class "ListItem"
    links = section.find_all('a', {'class': 'ListItem'})

    # Filter the links based on the href attribute that starts with "/upphandling/"
    upphandling_links = [link for link in links if link.get('href').startswith('/upphandling/')]

    # Print the href attribute of each link
    for link in upphandling_links:
        # print(link.get('href'))
        pass
    section = soup.find('section', {'role': 'complementary'})

    publicerat = section.find_all('p', {'class': 'Type-paragraph'})
    datum = [datum.text.strip() for datum in publicerat]
    publ_datum = datum[0::2]
    sista_ansokningsdag = datum[1::2]

    # Find all the links in the section that have the class "ListItem"
    links = section.select('a.ListItem')

    # Extract the href attribute of each link and store it in a list
    hrefs = [link['href'] for link in links]

    # Print the href attribute of each link
    article_links = []
    for href in hrefs:
        # print(urllib.parse('https://www.opic.com' + href, safe=':/'))
        # article_links.append(urllib.parse('https://www.opic.com' + href, safe=':/'))
        article_links.append('https://www.opic.com' + href)

    description = section.select("span.Type-paragraph.Type-paragraph--marginBn")

    descriptions = []

    for item in description:
        desc = item.text.strip()
        descriptions.append(desc)

    descriptions = list(filter(('Sista anbudsdag').__ne__, descriptions))
    descriptions = list(filter(('Sista ansökningsdag').__ne__, descriptions))
    descriptions = list(filter(('').__ne__, descriptions))
    #
    # ps = section.select('p.Type-paragraph.Type-paragraph--marginBn')
    #
    # times = []
    #
    # for item in ps:
    #     time = item.text.strip()
    #     times.append(time)


    df_list = [results, descriptions, publ_datum, sista_ansokningsdag, article_links]
    print(df_list)
    df = pd.DataFrame(df_list)
    df = df.T
    df.columns = ['Upphandling', 'Beställare', 'Publicerat', 'Senast_svar', 'Länk']

    return df

if __name__ == '__main__':
    df = get_articles("vibration")
    print(df)
    # print(tabulate(df.T))

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/

# print(tabulate(df.T))
# url = "https://www.opic.com/upphandlingar/sverige/?q=vibration&a=false"
# response = requests.get(url)
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# results = []
# section = soup.find('section', {'role': 'complementary'})


