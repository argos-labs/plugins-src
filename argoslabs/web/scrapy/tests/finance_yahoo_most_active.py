import scrapy
# import json
# noinspection PyPackageRequirements
from scrapy.crawler import CrawlerProcess

import sys
import csv
import logging
from scrapy.utils.log import configure_logging

# ################################################################################
# # noinspection PyUnusedLocal
# class JsonWriterPipeline(object):
#     # --------------------------------------------------------------------------
#     # noinspection PyAttributeOutsideInit
#     def open_spider(self, spider):
#         self.file = open('quoteresult.jl', 'w')
# 
#     # --------------------------------------------------------------------------
#     def close_spider(self, spider):
#         self.file.close()
# 
#     # --------------------------------------------------------------------------
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
# 
# 
# ################################################################################
# # noinspection PyUnusedLocal
# class ItemCollectorPipeline(object):
#     # --------------------------------------------------------------------------
#     def __init__(self):
#         self.ids_seen = set()
#         
#     # --------------------------------------------------------------------------
#     def process_item(self, item, spider):
#         items.append(item)


################################################################################
class MySpider(scrapy.Spider):
    name = 'finance_yahoo_most_active'
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )
    start_urls = ['https://finance.yahoo.com/most-active']
    
    custom_settings = {
        # 'LOG_LEVEL': logging.WARNING,
        # 'ITEM_PIPELINES':{'__main__.JsonWriterPipeline':1},
        # 'ITEM_PIPELINES': {'__main__.ItemCollectorPipeline': 100},
        # 'FEED_FORMAT': 'json',
        # 'FEED_URI': 'quoteresult.json',
    }
    header = (
        'symbol', 'name', 'price',
        'change', 'p_change', 'volume',
        'avg_vol_3m', 'market_cap', 'pe_ratio'
    )
    csv_writer = csv.writer(sys.stdout, lineterminator='\n')
    csv_writer.writerow(header)
    
    # --------------------------------------------------------------------------
    # noinspection PyMethodOverriding
    def parse(self, response):

        texts = response.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr//text()').getall()
        n_rows = len(texts) // 9
        for i in range(n_rows):
            row = (
                texts[i*9 + 0], texts[i*9 + 1], texts[i*9 + 2],
                texts[i*9 + 3], texts[i*9 + 4], texts[i*9 + 5],
                texts[i*9 + 6], texts[i*9 + 7], texts[i*9 + 8],
            )
            row_info = {
                'symbol': texts[i*9 + 0],
                'name': texts[i * 9 + 1],
                'price': texts[i * 9 + 2],
                'change': texts[i * 9 + 3],
                'p_change': texts[i * 9 + 4],
                'volume': texts[i * 9 + 5],
                'avg_vol_3m': texts[i * 9 + 6],
                'market_cap': texts[i * 9 + 7],
                'pe_ratio': texts[i * 9 + 8],
            }
            self.csv_writer.writerow(row)
            # print(row_info)
            yield row_info
        # //*[@id="scr-res-table"]/div[1]/table/tbody/tr//text()
        # # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[25]/td[1]/a
        # # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[1]/td[1]/a
        # symbols = response.xpath('//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[1]/a/text()').getall()
        # # //*[@id="scr-res-table"]/div[1]/table/tbody/tr[25]/td[2]/text()
        # names = response.css('//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[2]').getall()
        # prices = response.css('//*[@id="scr-res-table"]/div[1]/table/tbody/tr/td[3]/text()').getall()
        #
        # for item in zip(symbols, names, prices):
        #     scraped_info = {
        #         'symbols': item[0].strip(),
        #         'names': item[1].strip(),
        #         'prices': item[2].strip(),
        #     }
        #     yield scraped_info


################################################################################
# noinspection PyUnusedLocal,PyUnresolvedReferences
def main():
    from io import StringIO
    stderr = StringIO()
    org_stderr = sys.stderr
    sys.stderr = stderr
    process = CrawlerProcess({
        # "FEEDS": {"items.json": {"format": "json"}},
        # # "LOG_FILE": 'scrapy_log.txt',
        # "DOWNLOAD_DELAY": 3,
    })

    # MySpider.name = 'finance_yahoo_most_active'
    # MySpider.configure_logging(install_root_handler=False)
    # MySpider.logging.basicConfig(
    #     filename='log.txt',
    #     format='%(levelname)s: %(message)s',
    #     level=logging.INFO
    # )
    # MySpider.start_urls = ['https://finance.yahoo.com/most-active']

    process.crawl(MySpider)
    process.start()  # the script will block here until the crawling is finished
    sys.stderr = org_stderr


################################################################################
if __name__ == '__main__':
    main()
