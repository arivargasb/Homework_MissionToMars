
#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

#Site Navigation
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# Scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    title = article.find("div", class_="content_title").text
    content = article.find("div", class_ ="article_teaser_body").text
    output = [title, content]
    return output

# # JPL Mars Space Images - Featured Image
def marsImage():
    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# # Mars Weather
def marsWeather():
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    return weather

# # Mars Facts
def marsFacts():
    import pandas as pd
    mars_url = 'https://space-facts.com/mars/'
    browser.visit(mars_url)
    tables = pd.read_html(mars_url)
    df = tables[1]
    df.reset_index(drop=True)
    df.columns = ['Feature','Value']
    df.set_index(["Feature"])
    mars_facts =df.to_html('table.html')
    return mars_facts

# # Mars Hemispheres
def marsHem():
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    print(soup.prettify())
    # items that contain Mars hemispheres' information
    items = soup.find_all('div', class_='item')
    hemis_img_urls = []
    main_url = 'https://astrogeology.usgs.gov'
# loop through items
    for i in items: 
        title = i.find('h3').text # title
    
        part_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + part_img_url)
    
        part_img_html = browser.html
        soup = BeautifulSoup(part_img_html, 'html.parser')
        img_url = main_url + soup.find('img', class_='wide-image')['src']
        hemis_img_urls.append({"title" : title, "img_url" : img_url})
    
    # hemisphere_image_urls
    return hemis_img_urls
