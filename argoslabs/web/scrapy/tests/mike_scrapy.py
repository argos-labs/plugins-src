# noinspection PyPackageRequirements
import scrapy
import logging
import json
# noinspection PyPackageRequirements
from scrapy.crawler import CrawlerProcess
# import pandas as pd
# from pandas import read_csv
# import csv
# from scrapy.shell import inspect_response
# import numpy as np


################################################################################
# noinspection PyUnusedLocal
class JsonWriterPipeline(object):
    # --------------------------------------------------------------------------
    # noinspection PyAttributeOutsideInit
    def open_spider(self, spider):
        self.file = open('quoteresult.jl', 'w')

    # --------------------------------------------------------------------------
    def close_spider(self, spider):
        self.file.close()

    # --------------------------------------------------------------------------
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


################################################################################
# noinspection PyUnusedLocal
class ItemCollectorPipeline(object):
    # --------------------------------------------------------------------------
    def __init__(self):
        self.ids_seen = set()

    # --------------------------------------------------------------------------
    def process_item(self, item, spider):
        items.append(item)


################################################################################
class MySpider(scrapy.Spider):
    name = 'quotes'
# text file containing URLs from Crunchbase to be scraped
    with open('websites.txt') as f:
        start_urls = [url.strip() for url in f.readlines()]
    
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        # 'ITEM_PIPELINES':{'__main__.JsonWriterPipeline':1},
        'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline': 100},
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quoteresult.json',
    }
    
#    global count
    count = 0
    url_list = []
    
    # --------------------------------------------------------------------------
    # noinspection PyMethodOverriding
    def parse(self, response):
        # print('outVar',outVar)
        # print('count',self.count,'title text',response.xpath('//title/text()'))
        sitep = response.xpath('//p/text()').getall() # wow! this gets all text
        # print('sitep',sitep)
        subs = 'machine learning'
        result1 = [i for i in sitep if subs in i]
        if result1:  # boolean - list is not empty
            print('\n url',response.url)
            self.url_list.append(response.url)
            print('get title text', response.xpath('//title/text()').get())
            print('machine learning', result1, '\n')
#            yield response.url

        subs2 = 'brain'
        result1 = [i for i in sitep if subs2 in i]
        if result1:  # boolean - list is not empty
            print('\n url', response.url)
            self.url_list.append(response.url)
            print('get title text', response.xpath('//title/text()').get())
            print('brain',result1, '\n')
            
        subs3 = 'food'
        result1 = [i for i in sitep if subs3 in i]
        if result1: # boolean - list is not empty
            print('\n url', response.url)
            self.url_list.append(response.url)
            print('get title text', response.xpath('//title/text()').get())
            print('food', result1, '\n')
            
        # sitep_np = np.asarray(sitep)
#        print('sitep.shape',sitep_np.shape)
        self.count += 1
#        wait=input('pause')
#        print('get title text',response.xpath('//title/text()').get())
#        print("css version \n", response.css('title::text').get())
#        print('response.css \n',response.css)
#        inspect_response(response,self) ??
#        print('btn \n',response.css('a.btn::attr(href)').getall())


################################################################################
def main():
    out_var = 'outside_class'
    items = []
    process = CrawlerProcess({
        "FEEDS": {"items.json": {"format": "json"}},
        # "LOG_FILE": 'scrapy_log.txt',
        "DOWNLOAD_DELAY": 3,
    })

    process.crawl(MySpider)
    process.start()  # the script will block here until the crawling is finished
    for item in items:
        print('item', item)


################################################################################
if __name__ == '__main__':
    main()
