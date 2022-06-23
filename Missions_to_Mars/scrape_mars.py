# %%
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import time
import pandas as pd


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the parent divs for all articles
    results = soup.find_all('div', class_="list_text")

    results[0].find_all('div',class_='article_teaser_body')[0].text

    for result in results:
    #scarpe the article header
        news_title = result.find_all('div',class_='content_title')[0].text
        news_p = result.find_all('div',class_='article_teaser_body')[0].text

    # Dictionary 
    post = {
        'title': news_title,
        'parap': news_p,
    }

    # Visit https://spaceimages-mars.com/
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the parent divs for all articles
    img_result = soup.find_all('img', class_="headerimage fade-in")

    featured_image_url = img_result[0]['src']

    # Use pandas to scrape website
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    # Convert the data to a HTML table string
    html_table = tables[1].to_html()

    url = 'https://marshemispheres.com/index.html'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the parent divs for product
    results = soup.find_all('div', class_="description")

    url_lst = []

    for result in results:
        #Scrape all the the URLS for each of the soruce
        url_lst.append(result.find('a')['href'])

    book_url_list = ['https://marshemispheres.com/' + url for url in url_lst]
    title_lst = [url.split('.html')[0] + ' Hemisphere' for url in url_lst]

    i = 0

    hemisphere_image_urls = []

    for title_url in book_url_list:
        browser.visit(title_url)
        html = browser.html
        soup = bs(html, "html.parser")

        results = soup.find_all('div', class_="downloads")
        img_link =  'https://marshemispheres.com/' + results[0].find('a')['href']

        print(title_lst[i], img_link)

        # Data to export
        mars_hemisphere_data = {
            "title": title_lst[i],
            "img_url": img_link,
        }

        hemisphere_image_urls.append(mars_hemisphere_data)

        i += 1

    browser.quit()

    return


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

scrape()