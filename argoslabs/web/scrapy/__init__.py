"""
====================================
 :mod:`argoslabs.web.scrapy`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module web bsoup using BeautifulSoup
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/07/31]
#     - Change group "9: Utility Tools" => "10: Web Scraping"
#  * [2021/04/12]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/10/09]
#     - add --parameters
#       * Note for parameter passing Script or URLs
#         1. Change { => {{, } => }}
#         2. placeholder for "{param1}" and STU property add parameter
#             like "param1::=value1"
#  * [2020/10/07]
#     - starting

################################################################################
import os
import re
import sys
import time
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
# noinspection PyUnresolvedReferences,PyPackageRequirements
import scrapy
# noinspection PyUnresolvedReferences,PyPackageRequirements
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from io import StringIO
from multiprocessing import Process, Queue
# noinspection PyPackageRequirements
from twisted.internet import reactor


################################################################################
START_URLS = None


# ################################################################################
# # the wrapper to make it run more times
# def run_spider(spider):
#     # noinspection PyUnresolvedReferences,PyShadowingNames
#     def f(q):
#         try:
#             runner = CrawlerRunner()
#             deferred = runner.crawl(spider)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             # time.sleep(0.5)
#             q.put(None)
#         except Exception as e:
#             q.put(e)
#
#     q = Queue()
#     p = Process(target=f, args=(q, spider, ))
#     p.start()
#     # time.sleep(0.5)
#     result = q.get()
#     p.join()
#
#     if result is not None:
#         raise result


################################################################################
@func_log
def do_scrapy(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    process = None
    try:
        if not os.path.exists(argspec.script):
            raise IOError(f'Cannot read Scrapy Script file "{argspec.script}"')
        with open(argspec.script, encoding=argspec.encoding) as ifp:
            script = ifp.read()
        rm = re.search(r'class\s+([_\w]+)\(scrapy\.Spider\):', script, re.MULTILINE)
        if rm is None:
            raise ValueError(f'In script Spider class must be defined like '
                             f'"class MySpider(scrapy.Spider):"')
        gdict = globals()
        # noinspection PyTypeChecker
        spider_name = rm.groups(1)[0]
        imps = re.findall(r'(^|\n)(import|from)\s+([_\w]+)', script, re.MULTILINE)
        for _, _, imp_name in imps:
            gdict[imp_name] = __import__(imp_name)

        urls = list()
        urls.extend(argspec.urls)
        if argspec.url_file and os.path.exists(argspec.url_file):
            with open(argspec.url_file, 'r', encoding=argspec.encoding) as ifp:
                urls.extend(
                    [line.strip() for line in ifp if line]
                )
        if not urls:
            raise ValueError(f'Invalid Start URLs or URL file')

        if argspec.parameters:
            try:
                params = {}
                for pl in argspec.parameters:
                    k, v = pl.split('::=', maxsplit=1)
                    params[k] = v
                if params:
                    script = script.format(**params)
                    for i in range(len(urls)):
                        urls[i] = urls[i].format(**params)
            except Exception:
                raise ReferenceError('''parameter passing Script or URLs Error:
1. Change { => {{, } => }}
2. Placeholder for "{param1}" and STU property add parameter''')

        global START_URLS
        START_URLS = urls
        ldict = {}
        exec(script, gdict, ldict)
        spider = ldict[spider_name]

        stderr = StringIO()
        org_stderr = sys.stderr
        sys.stderr = stderr

        process = CrawlerProcess({
            # "DOWNLOAD_DELAY": 3,
        })
        process.crawl(spider)
        # the script will block here until the crawling is finished
        process.start(stop_after_crawl=True)
        process.join()

        # run_spider(spider)

        sys.stderr = org_stderr
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        if process is not None:
            process.stop()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='10',  # Web Scraping
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Scrapy Basic',
        icon_path=get_icon_path(__file__),
        description='''Scrapy tool basic''',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('script',
                          display_name='Scrapy Script',
                          input_method='fileread',
                          help='Scrapy Script')

        # ##################################### for app dependent options
        mcxt.add_argument('--urls',
                          display_name='Start URLs', action='append',
                          show_default=True,
                          help='Starting URLs for scrapy')
        mcxt.add_argument('--url-file',
                          display_name='Start URL file',
                          input_method='fileread',
                          show_default=True,
                          help='Text file which contains URLs by line')
        mcxt.add_argument('--parameters',
                          display_name='Parameters', action='append',
                          help='Parameters passing to Scirpt or URLs. Format is '
                               '"key::=value". Place holder is "{key}"')
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for files, default is [[utf-8]]')

        argspec = mcxt.parse_args(args)
        return do_scrapy(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
