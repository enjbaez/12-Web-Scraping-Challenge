# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

http://localhost:8889/edit/GT-ATL-DATA-PT-12-2019-U-C/DataViz-Content/10-Advanced-Data-Storage-and-Retrieval/3/Activities/04-Ins_First_Steps_with_Flask/Solved/app.py

# import all dependencies
# if __name__ == "__main__":
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape ():
    """Scrapes NASA and Twitters websites for information about Mars"""
    
    browser = init_browser()
    mars_data = {}

    # visit the NASA Mars News site and scrape headlines
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    time.sleep(5)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    nasa_headline = first_item.find('div', class_='content_title').text
    nasa_teaser = first_item.find('div', class_='article_teaser_body').text
    mars_data["nasa_headline"] = nasa_headline
    mars_data["nasa_teaser"] = nasa_teaser

    # visit the JPL website and scrape the featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        time.sleep(5)

        jpl_html = browser.html
        jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

        img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
        image_path = f'https://www.jpl.nasa.gov{img_relative}'
        mars_data["feature_image_src"] = image_path
    except ElementNotVisibleException:
        image_path = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22076_hires.jpg'
        mars_data["feature_image_src"] = image_path
        
    # Scrape latest Mars Tweet
    mars_tweets_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_tweets_url)
    time.sleep(5)
    mars_tweets_html = browser.html
    mars_tweets_soup = BeautifulSoup(mars_tweets_html, 'html.parser')

    mars_weather_tweet = mars_tweets_soup.find_all('article')
    for x in mars_weather_tweet:
    tweet = x.find("div",attrs={"data-testid":"tweet"})
    tweet_list=tweet.find("div",class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    for j in tweet_list:
        print(j.parent.text)


  # Scrape Mars facts table
  mars_facts_url = 'https://space-facts.com/mars/'
  browser.visit(mars_facts_url)
  time.sleep(5)
  mars_facts_html = browser.html
  mars_facts_soup = BeautifulSoup(mars_facts_html, 'html.parser')

  mars_facts_soup.body.find_all('table', class_="tablepress tablepress-id-p-mars")

    # scrape images of Mars' hemispheres from the USGS site
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_dicts = []

    for i in range(1,9,2):
        hemi_dict = {}
        
        browser.visit(mars_hemisphere_url)
        time.sleep(5)
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
        hemi_name = hemi_name_links[i].text.strip('Enhanced')
        
        detail_links = browser.find_by_css('a.product-item')
        detail_links[i].click()
        time.sleep(5)
        browser.find_link_by_text('Sample').first.click()
        time.sleep(5)
        browser.windows.current = browser.windows[-1]
        hemi_img_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
        
        hemi_img_soup = BeautifulSoup(hemi_img_html, 'html.parser')
        hemi_img_path = hemi_img_soup.find('img')['src']

        hemi_dict['title'] = hemi_name.strip()       
        hemi_dict['img_url'] = hemi_img_path

        hemi_dicts.append(hemi_dict)

    mars_data["hemisphere_imgs"] = hemi_dicts

    browser.quit()

    return mars_data