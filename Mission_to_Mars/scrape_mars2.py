#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import our dependencies

import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser


# In[2]:


# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

mars_data = {}

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

browser.visit(url1)

html1 = browser.html
soup1 = BeautifulSoup(html1, 'html.parser')




# In[5]:


# Collect latest news title and save it to a variable

results = soup1.find_all('div', class_="content_title")


# In[8]:


latest = results[0]
mars_data["latest_title"] = latest.a.text.strip()


# In[10]:


# Collect latest news paragraph and save it to a variable
results2 = soup1.find_all('div', class_="rollover_description_inner")


# In[12]:


paragraphs = []

for row in results2:
    paragraphs.append(row.text)

mars_data["latest_p"] = paragraphs[0].strip()


# In[13]:


# JPL Mars Space Images - Featured Image - Jake Matijevic Rock

url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)


# In[17]:


html2 = browser.html
soup2 = BeautifulSoup(html2, 'html.parser')
articles = soup2.find_all('article',class_="carousel_item")
    
for article in articles:
    link = article.find('a')
    href = link['data-fancybox-href']


# In[20]:


mars_data["featured_image_url"] = 'https://www.jpl.nasa.gov' + href


# In[21]:


# Scrape 'Mars Weather' Twitter Account - Weather in latest tweet

url3 = 'https://twitter.com/marswxreport?lang=en'

browser.visit(url3)

html3 = browser.html
soup3 = BeautifulSoup(html3, 'html.parser')


# In[22]:


results3 = soup3.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")


# In[30]:


weather = []

for row in results3:
    weather.append(row.text)

mars_data["mars_weather"] = weather[0].replace('\n',', ').replace('pic.twitter.com/','.')


# In[31]:


# Scrape Mars Facts website for table to pandas dataframe - convert pandas df to html

url4 = 'https://space-facts.com/mars/'
tables = pd.read_html(url4)
mars_table = tables[0]
mars_table2 = mars_table.rename(columns={0:"Description",1:"Value"}).set_index("Description")


# In[32]:


mars_table2.to_html('mars_facts.html')
mars_html_table = mars_table2.replace("\n", "")
mars_data["mars_facts"] = mars_html_table


# In[15]:


# Mars Hemispheres

#'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# In[33]:


url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

browser.visit(url5)

html3 = browser.html
soup4 = BeautifulSoup(html3, 'html.parser')


# In[36]:


mars_data["cerb_title"] = soup4.find_all('h2')[0].text
cerb_img = soup4.find_all('div',class_="wide-image-wrapper")
for images in cerb_img:
    link = images.find('a')
    mars_data["cerb_jpg"] = link['href']


# In[37]:


url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

browser.visit(url6)

html4 = browser.html
soup5 = BeautifulSoup(html4, 'html.parser')


# In[40]:


mars_data["schi_title"] = soup5.find_all('h2')[0].text
schi_img = soup5.find_all('div',class_="wide-image-wrapper")
for images in schi_img:
    link = images.find('a')
    mars_data["schi_jpg"] = link['href']


# In[41]:


url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

browser.visit(url7)

html5 = browser.html
soup6 = BeautifulSoup(html5, 'html.parser')


# In[43]:


mars_data["syr_title"] = soup6.find_all('h2')[0].text
syr_img = soup6.find_all('div',class_="wide-image-wrapper")
for images in syr_img:
    link = images.find('a')
    mars_data["syr_jpg"] = link['href']


# In[44]:


url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

browser.visit(url8)

html6 = browser.html
soup7 = BeautifulSoup(html6, 'html.parser')


# In[45]:


mars_data["vall_title"] = soup7.find_all('h2')[0].text
vall_img = soup7.find_all('div',class_="wide-image-wrapper")
for images in vall_img:
    link = images.find('a')
    mars_data["vall_jpg"] = link['href']


# In[46]:


mars_data


# In[ ]:





# In[ ]:




