#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# ## Step 1 - Scraping

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)

#  dictionary that can be imported into Mongo
mars_info = {}

# ### NASA Mars News

def mars_news():
    try: 
        browser = init_browser()
        news_url = "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        article = soup.find("div", class_='list_text')
        title = article.find("div", class_="content_title").text
        content = article.find("div", class_ ="article_teaser_body").text
        mars_info['news_title'] = title
        mars_info['news_paragraph'] = content
        return mars_info
    finally:
        browser.quit()

### JPL Mars Space Images - Featured Image

def mars_images():
    try: 
        browser = init_browser()
        images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(images_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        image = soup.find("img", class_="thumb")["src"]
        featured_image_url = "https://www.jpl.nasa.gov" + image
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        mars_info['featured_image_url'] = featured_image_url 
        return mars_info
    finally:
        browser.quit()

# # ### Mars Weather

def mars_weather():
    try: 
        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
        mars_info['weather'] = weather
        return mars_weather
    finally:
        browser.quit()


# # ### Mars Facts

def mars_facts():
    mars_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(mars_url)
    df = tables[1]
    df.reset_index(drop=True)
    df.columns = ['Feature','Value']
    df.set_index(["Feature"])
    data = df.to_html('table.html')
    mars_info['mars_facts'] = data
    return mars_info

# ### Mars Hemispheres

def mars_hemispheres():
    try:
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')
        hemis_img_urls = []
        main_url = 'https://astrogeology.usgs.gov'
        
        for i in items: 
            title = i.find('h3').text # title
            part_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(main_url + part_img_url)
            part_img_html = browser.html
            soup = BeautifulSoup(part_img_html, 'html.parser')
            img_url = main_url + soup.find('img', class_='wide-image')['src']
            hemis_img_urls.append({"title" : title, "img_url" : img_url})
        
        mars_info['hemispheres'] = hemis_img_urls
        return mars_info
    finally:
        browser.quit()






