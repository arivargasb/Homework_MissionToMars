#!/usr/bin/env python
# coding: utf-8

# In[152]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# ## Step 1 - Scraping

# In[153]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)


# ### NASA Mars News

# In[95]:


news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[30]:


article = soup.find("div", class_='list_text')
title = article.find("div", class_="content_title").text
content = article.find("div", class_ ="article_teaser_body").text
# print(article)
print("Title: " + title)
print("Content: " + summary)


# ### JPL Mars Space Images - Featured Image

# In[96]:


images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(images_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[72]:


image = soup.find("img", class_="thumb")["src"]
featured_image_url = "https://www.jpl.nasa.gov" + image
print(featured_image_url)


# ### Mars Weather

# In[99]:


weather_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(weather_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[110]:


weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
print(weather)


# ### Mars Facts

# In[114]:


mars_url = 'https://space-facts.com/mars/'


# In[116]:


tables = pd.read_html(mars_url)
tables


# In[136]:


type(tables)


# In[145]:


df = tables[1]
df.reset_index(drop=True)
df.columns = ['Feature','Value']
df.set_index(["Feature"])


# In[148]:


df.to_html('table.html')


# ### Mars Hemispheres

# In[154]:


hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemispheres_url)


# In[159]:


html_hemispheres = browser.html
soup = BeautifulSoup(html_hemispheres, 'html.parser')
print(soup.prettify())
# items that contain Mars hemispheres' information
items = soup.find_all('div', class_='item')


# In[164]:


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
hemis_img_urls


# ## Step 2 - MongoDB and Flask Application

# In[ ]:




