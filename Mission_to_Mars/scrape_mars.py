#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import our dependencies

import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser


# In[2]:


# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/Mitchell Capell/Desktop/web-scraping-challenge/Mission_to_Mars/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    mars_data = {}

    url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    response1 = requests.get(url1)

    soup1 = BeautifulSoup(response1.text,'html.parser')


# In[3]:


# Collect latest news title and save it to a variable

    results = soup1.find_all('div', class_="content_title")


# In[4]:


    latest = results[0]
    mars_data["latest_title"] = latest.a.text.strip()


# In[5]:


# Collect latest news paragraph and save it to a variable
    results2 = soup1.find_all('div', class_="rollover_description_inner")


# In[6]:


    paragraphs = []

    for row in results2:
        paragraphs.append(row.text)

    mars_data["latest_p"] = paragraphs[0].strip()


# In[7]:


# JPL Mars Space Images - Featured Image - Jake Matijevic Rock

    browser = init_browser()

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)


# In[8]:


    for x in range(0,1):

        html = browser.html
        soup2 = BeautifulSoup(html, 'html.parser')
        articles = soup2.find_all('article',class_="carousel_item")
    
    for article in articles:
        link = article.find('a')
        href = link['data-fancybox-href']


# In[9]:


    mars_data["featured_image_url"] = 'https://www.jpl.nasa.gov' + href

    browser.quit()


# In[10]:


# Scrape 'Mars Weather' Twitter Account - Weather in latest tweet

    url3 = 'https://twitter.com/marswxreport?lang=en'

    response2 = requests.get(url3)

    soup3 = BeautifulSoup(response2.text,'html.parser')


# In[11]:


    results3 = soup3.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")


# In[12]:


    weather = []

    for row in results3:
        weather.append(row.text)

    mars_data["mars_weather"] = weather[0].replace('\n',', ').replace('pic.twitter.com/NO4iCrXgrl','.')


# In[13]:


# Scrape Mars Facts website for table to pandas dataframe - convert pandas df to html

    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_table = tables[0]
    mars_table2 = mars_table.rename(columns={0:"Description",1:"Value"}).set_index("Description")


# In[14]:


    mars_table2.to_html('mars_facts.html')
    mars_html_table = mars_table2.replace("\n", "")
    mars_data["mars_facts"] = mars_html_table


# In[15]:


# Mars Hemispheres

#'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[16]:


    url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

    response3 = requests.get(url5)

    soup4 = BeautifulSoup(response3.text,'html.parser')


# In[17]:


    mars_data["cerb_title"] = soup4.find_all('h2')[0].text
    cerb_img = soup4.find_all('div',class_="wide-image-wrapper")
    for images in cerb_img:
        link = images.find('a')
        mars_data["cerb_jpg"] = link['href']


# In[18]:


    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

    response4 = requests.get(url6)

    soup5 = BeautifulSoup(response4.text,'html.parser')


# In[19]:


    mars_data["schi_title"] = soup5.find_all('h2')[0].text
    schi_img = soup5.find_all('div',class_="wide-image-wrapper")
    for images in schi_img:
        link = images.find('a')
        mars_data["schi_jpg"] = link['href']


# In[20]:


    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

    response5 = requests.get(url7)

    soup6 = BeautifulSoup(response5.text,'html.parser')


# In[21]:


    mars_data["syr_title"] = soup6.find_all('h2')[0].text
    syr_img = soup6.find_all('div',class_="wide-image-wrapper")
    for images in syr_img:
        link = images.find('a')
        mars_data["syr_jpg"] = link['href']


# In[22]:


    url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    response6 = requests.get(url8)

    soup7 = BeautifulSoup(response6.text,'html.parser')


# In[23]:


    mars_data["vall_title"] = soup7.find_all('h2')[0].text
    vall_img = soup7.find_all('div',class_="wide-image-wrapper")
    for images in vall_img:
        link = images.find('a')
        mars_data["vall_jpg"] = link['href']
    


# In[24]:


    return mars_data


# In[ ]:
# In[ ]:




