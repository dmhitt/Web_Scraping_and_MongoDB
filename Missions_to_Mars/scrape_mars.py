from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Nasa Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    quotes = soup.find_all('div', class_='content_title')

    news_title = quotes[0].text
    #print(news_title)
 
    quotes = soup.find_all('div', class_='article_teaser_body')

    news_p = quotes[0].text
    #print(news_p)

    # JPL Mars Space Images

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    quotes = soup.find_all('div', class_='floating_text_area')
    link = quotes[0].a['href']
    featured_image_url = url + "/" +link
    #print(featured_image_url)

    # Mars Facts
    url = 'https://galaxyfacts-mars.com/'

    time.sleep(1)

    tables = pd.read_html(url)
    df = tables[0]

    df = df.iloc[1: , :]

    df = df.rename(columns={0:"Mars - Earth Comparison",
                        1:"Mars",
                        2:"Earth"})

    df = df.reset_index(drop=True)
    df.set_index("Mars - Earth Comparison",inplace=True)

    html_table = df.to_html()
    df.to_html('table.html')

    # Mars Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)  
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls = []


    quotes = soup.find_all('div', class_='item')
    #print (quotes)
    ind = 0
    for quote in quotes:
        hm = {}
        hm['title']= quote.h3.text
        link = url + quote.a['href']
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        quotes2 = soup.find('img', class_='wide-image')
        #print(quotes2)
        src = url + quotes2["src"]
        #print (src)
        hm['img_url']= src
        hemisphere_image_urls.append(hm)
    
    #print(hemisphere_image_urls)    

    # Store data in a dictionary
    mars_data = {
        'news_title': news_title, 
        'news_p':  news_p, 
        'featured_image_url': featured_image_url,
        'html_table': html_table,
        'hemisphere_image_urls' : hemisphere_image_urls
    }

    browser.quit()

    # Return results
    return mars_data
