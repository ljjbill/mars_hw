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
    nasa_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(nasa_image)
    tmd.sleep(2)

    from urllib.parse import urlsplit
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(nasa_image))
    
    xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

    #Use splinter to click on the mars featured image
    #to bring the full resolution image
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()
    tmd.sleep(2)
    
    #get image url using BeautifulSoup
    html_image = browser.html
    soup = bs(html_image, "html.parser")
    img_url = soup.find("img", class_="fancybox-image")["src"]
    full_img_url = base_url + img_url
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
