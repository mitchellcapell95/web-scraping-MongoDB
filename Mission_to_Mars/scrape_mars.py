
#Import our dependencies

import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser


# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later.

def init_browser():
    executable_path = {'executable_path': '/Users/Mitchell Capell/Desktop/web-scraping-challenge/Mission_to_Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    mars_data = {}

    url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    browser.visit(url1)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'html.parser')

# Collect latest news title and save it to a variable

    results = soup1.find_all('div', class_="content_title")


    latest = results[0]
    mars_data["latest_title"] = latest.a.text.strip()


# Collect latest news paragraph and save it to a variable
    results2 = soup1.find_all('div', class_="rollover_description_inner")

    paragraphs = []

    for row in results2:
        paragraphs.append(row.text)

    mars_data["latest_p"] = paragraphs[0].strip()

# JPL Mars Space Images 

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url2)

    featured_url = []

    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')
    fancybox = soup2.find_all('a',class_="fancybox")

    for fancy in fancybox:
        featured_url.append(fancy['data-fancybox-href'])
    href = featured_url[1]

    mars_data["featured_image_url"] = 'https://www.jpl.nasa.gov' + href

# Scrape 'Mars Weather' Twitter Account - Weather in latest tweet

    url3 = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url3)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, 'html.parser')

    results3 = soup3.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    weather = []

    for row in results3:
        weather.append(row.text)

    mars_data["mars_weather"] = weather[0].replace('\n',', ')

# Scrape Mars Facts website for table to pandas dataframe - convert pandas df to html

    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    mars_table = tables[0]
    mars_table2 = mars_table.rename(columns={0:"Description",1:"Value"}).set_index("Description")

    mars_html_table = mars_table2.to_html().replace("\n", "")

    mars_data["mars_facts"] = mars_html_table

    url5 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

    browser.visit(url5)

    html3 = browser.html
    soup4 = BeautifulSoup(html3, 'html.parser')

    first_title = soup4.find_all('h2')[0].text
    cerb_img = soup4.find_all('div',class_="wide-image-wrapper")
    for images in cerb_img:
        link = images.find('a')
        first_url = link['href']


    url6 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'

    browser.visit(url6)

    html4 = browser.html
    soup5 = BeautifulSoup(html4, 'html.parser')

    second_title = soup5.find_all('h2')[0].text
    schi_img = soup5.find_all('div',class_="wide-image-wrapper")
    for images in schi_img:
        link = images.find('a')
        second_url = link['href']


    url7 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'

    browser.visit(url7)

    html5 = browser.html
    soup6 = BeautifulSoup(html5, 'html.parser')

    third_title = soup6.find_all('h2')[0].text
    syr_img = soup6.find_all('div',class_="wide-image-wrapper")
    for images in syr_img:
        link = images.find('a')
        third_url = link['href']

    url8 = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'

    browser.visit(url8)

    html6 = browser.html
    soup7 = BeautifulSoup(html6, 'html.parser')

    fourth_title = soup7.find_all('h2')[0].text
    vall_img = soup7.find_all('div',class_="wide-image-wrapper")
    for images in vall_img:
        link = images.find('a')
        fourth_url = link['href']

    hemisphere_image_urls = [
            {'title': first_title, 'img_url': first_url},
            {'title': second_title, 'img_url': second_url},
            {'title': third_title, 'img_url': third_url},
            {'title': fourth_title, 'img_url': fourth_url}
        ]

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    
    browser.quit()

    return mars_data
