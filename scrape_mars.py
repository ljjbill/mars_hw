#import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import pandas as pd
import time as tmd
from selenium import webdriver

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
    

def scrape():
    browser = init_browser()
    mars_facts_data = {}

    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    tmd.sleep(2)

    html = browser.html
    soup = bs(html,"html.parser")

    #scrapping latest news about mars from nasa
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = news_paragraph 
    
    #Mars Featured Image
    #Define the URL of the image page
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    #Visit the URL via chrome
    browser.visit(url_image)
    tmd.sleep(2)

    #Get the html codes of the page
    html_image = browser.html
    #Parse the html codes
    soup = bs(html_image, "html.parser")
    #Find the image url
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    #Define the base url
    base_url = 'https://www.jpl.nasa.gov'
    #Combine two url into one
    full_img_url = base_url + featured_image_url
    mars_facts_data["featured_image"] = full_img_url
    
    # #### Mars Weather

    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')

    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'hPa' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass
    mars_facts_data["mars_weather"] = weather_tweet

    # #### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    tmd.sleep(2)
    table = pd.read_html(url_facts)
    table[0]

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    clean_table = df_mars_facts.set_index(["Parameter"])
    mars_html_table = clean_table.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_facts_data["mars_facts_table"] = mars_html_table

    # #### Mars Hemisperes

    
    # Visit the USGS Astogeology site and scrape pictures of the hemispheres
    url_usgs = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_usgs)

    # Use splinter to loop through the 4 images and load them into a dictionary
    import time 
    html = browser.html
    soup = bs(html, 'html.parser')
    hemisphere_image_urls=[]

    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        tmd.sleep(2)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"image title":img_title,"image url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
    print(hemisphere_image_urls)

    mars_facts_data["hemisphere_img_url"] = hemisphere_image_urls

    

    return mars_facts_data
