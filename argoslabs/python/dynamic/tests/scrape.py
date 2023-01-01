# ###### Webscrape_v5 - borrowed from v5 indent error problem in myspider
# https://stackoverflow.com/questions/57616611/python-scrapy-issues-running-imagespipeline-when-running-crawler-from-scrip


################################################################################
import os
import re
import sys
import csv
import scrapy
import datetime
from scrapy.crawler import CrawlerProcess
# from scrapy.pipelines.images import ImagesPipeline
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


################################################################################
class ItemSearch(scrapy.Item):
    # ==========================================================================
    Organization = scrapy.Field()
    url = scrapy.Field()
    search = scrapy.Field()
    result = scrapy.Field()


################################################################################
# noinspection PyUnresolvedReferences
class MySpider(scrapy.Spider):
    # ==========================================================================
    name = "MySpider"
    rec1 = re.compile(r'[ \t]+')
    rec2 = re.compile(r'[\n \t]+')
    rec3 = re.compile(r'[^a-zA-Z ]+')

    # ==========================================================================
    @staticmethod
    def get_nomalized_url(url):
        url = ':'.join(url.split(':', maxsplit=1)[1:])
        if url[-1] == '/':
            url = url[:-1]
        if url.startswith('//www.'):
            url = '//' + url[6:]
        return url

    # ==========================================================================
    def _get_body_text(self, response, org):
        # sitep = response.xpath('//p/text()').getall()
        # https://stackoverflow.com/questions/23156780/how-can-i-get-all-the-plain-text-from-a-website-with-scrapy
        try:
            bodytext = ''.join(response.xpath("//body//text()").extract()).strip().lower()
            bodytext = self.rec1.sub(' ', bodytext)
            bodytext = self.rec2.sub('\n', bodytext)
        except Exception:
            return '', '', ''
        bodytext_f = os.path.join(self.p_output_folder, self.rec3.sub("", org) + '.txt')
        with open(bodytext_f, 'wb') as ofp:
            ofp.write(str.encode(bodytext))
        return bodytext, bodytext_f

    # ==========================================================================
    def parse(self, response):
        item = ItemSearch()
        org = response.meta.get('org')
        bodytext, bodytext_f = self._get_body_text(response, org)
        if bodytext and bodytext_f and org:
            found_s = list()
            for search in self.p_searchs:
                search = search.lower()
                if bodytext.find(search) >= 0:
                    found_s.append(search)
            if found_s:
                self.cw.writerow([
                    org,
                    response.url,
                    '|'.join(found_s),
                    bodytext_f
                ])
                item['search'] = found_s
                item['url'] = response.url
                yield item

    # ==========================================================================
    def start_requests(self):
        for u in self.start_urls:
            nz_url = self.get_nomalized_url(u)
            if nz_url not in self.org_ref:
                self.logger.error('Cannot find org text from url ' + response.url)
                return bodytext, '', ''
            org = self.org_ref[nz_url]
            meta = dict()
            meta['org'] = org
            yield scrapy.Request(u, meta=meta, errback=self.errback_httpbin)

    # ==========================================================================
    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)


################################################################################
def scrapy_main(input_csv, output_folder, searchs):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    stderr_f = os.path.join(output_folder, 'MySpider-%s.log' % (datetime.datetime.now().strftime("%Y%m%d-%H%M"),))
    stderr = open(stderr_f, 'w')
    o_stderr = sys.stderr
    sys.stderr = stderr
    try:
        MySpider.p_searchs = eval(searchs)
        MySpider.p_output_folder = output_folder

        start_urls = list()
        org_ref = dict()
        with open(input_csv, encoding='utf-8') as ifp:
            reader = csv.reader(ifp)
            for i, row in enumerate(reader):
                if i < 1:
                    continue
                url = row[7].strip()
                if not url:
                    continue
                start_urls.append(url)
                nz_url = MySpider.get_nomalized_url(url)
                org_ref[nz_url] = row[0].strip()
        MySpider.start_urls = start_urls
        MySpider.org_ref = org_ref
        MySpider.cw = csv.writer(sys.stdout, lineterminator='\n')
        MySpider.cw.writerow([
            'org',
            'url',
            'found',
            'output_file'
        ])
        settings = dict()
        settings['DOWNLOAD_DELAY'] = 3
        process = CrawlerProcess(settings)
        process.crawl(MySpider)
        process.start()  # the script will block here until the crawling is finished
    finally:
        stderr.close()
        sys.stderr = o_stderr
        pass


################################################################################
if __name__ != '__main__':
    _searches = '{searches}'
    _input = '{input}'
    _output_folder = r'{output_folder}'
    scrapy_main(_input, _output_folder, _searches)
else:
    _searches = '["machine learning", "brain", "food", "robot"]'
    _input = 'companies-10.csv'
    _output_folder = 'output'
    scrapy_main(_input, _output_folder, _searches)
