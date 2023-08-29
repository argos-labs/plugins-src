#!/usr/bin/env python
# coding: utf-8

# Using tutorial https://www.youtube.com/watch?v=ogPMCpcgb-E
# scrapes cat images from reddit.
# try for images on startup pages, etc.

# In[1]:


import scrapy
import logging
import json
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import pandas as pd
from pandas import read_csv
import csv
from scrapy.shell import inspect_response
import numpy as np
from scrapy.pipelines.images import ImagesPipeline


# In[2]:


IMAGES_STORE = 'images'
BOT_NAME = 'ImgScrapy'


# In[3]:


class RedditSpider(scrapy.Spider):
    name = "reddit"
    start_urls = ["http://www.skyfront.com"]
#    start_urls = ["https://www.reddit.com/r/cats"]
# read crunchbase file and pick off websites
    dataset1=read_csv('C:/Users/MStopa/WebScraping&Crunchbase/WebScraping&Crunchbase/Crunchbase/companies-8-21-2020.csv')
    df=dataset1[['Organization Name','Headquarters Location','Website']]
    start_urlsA=df['Website'].to_numpy().tolist()
#    start_urls=start_urlsA[6:8]
#    start_urls+=["http://www.skyfront.com"]
    companies=df['Organization Name'].to_numpy().tolist()
    print('start_urls here',start_urls)
    
    def parse(self, response):
        links = response.xpath("//img/@src  | //img/@alt")
        links2 = response.xpath("//img/@data-src | //img/@alt")
        html = ""
        print("links2",links2[9]," \n",links2[10]," \n",links2[11]," \n",links2[12])
        
        link_count=-1
        
        for link in links2:
            link_count+=1
            linkB=links2[link_count+1] # the following links2 is the alternative text or alt
            url = link.get() # get extracts the textual data from the selector
            urlB = linkB.get() # thus urlB contains the alt part of the link

# triple quotes is python for multi-line complex strings, only things in braces 
# get replace by values from the format statement.
            if any(ext in url for ext in [".jpg", ".gif", ".png"]): # ext is not a keyword
                html_plus = """<a href="{url}" 
                target="_blank">
                <img src="{url}" height="33%" width="33%" alt="{urlB}" > <figcaption>
                "{urlB}" </figcaption> <a/""".format(url=url,urlB=urlB)
                html += html_plus
                print("html_plus",html_plus)
                
                with open("frontpage.html", "a") as page:
                    page.write(html)
                    page.close()


# In[4]:


if __name__ == "__main__":

    items=[]
    process = CrawlerProcess({
    })
    process.crawl(RedditSpider)
    process.start()
    
    for item in items:
        print('item',item)


# In[ ]:




