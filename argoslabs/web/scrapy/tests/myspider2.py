
import sys
import csv
import scrapy
from random import randint

################################################################################
class MySpider(scrapy.Spider):
    name = 'finance_yahoo_most_active'
    start_urls = START_URLS
    
    custom_settings = {{
    }}

    header = (
        '{symbol}', '{name}', 'price',
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
            row_info = {{
                '{symbol}': texts[i*9 + 0],
                '{name}': texts[i * 9 + 1],
                'price': texts[i * 9 + 2],
                'change': texts[i * 9 + 3],
                'p_change': texts[i * 9 + 4],
                'volume': texts[i * 9 + 5],
                'avg_vol_3m': texts[i * 9 + 6],
                'market_cap': texts[i * 9 + 7],
                'pe_ratio': texts[i * 9 + 8],
            }}
            self.csv_writer.writerow(row)
            yield row_info
