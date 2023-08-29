"""
====================================
 :mod:`argoslabs.api.rossum`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS Rossum API module
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/26]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/03/19]
#     - CSV 출력 점검
#  * [2019/12/05]
#     - 새로운 API에 맞춰 다시 작업
#  * [2019/03/27]
#     - 경우에 따라 오래 걸리면서 json 결과를 만들고 멈추어 있는 상태 처리
#  * [2019/03/21]
#     - starting

################################################################################
import os
import re
import sys
import time
import json
import datetime
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class RossumApi(object):
    V1_API = 'https://api.elis.rossum.ai/v1'
    OUTPUT_FORMATS = [
        'json',
        'csv',
        'xml',
    ]

    # ==========================================================================
    def __init__(self, userid, passwd, queue_name=None,
                 result_format='json', timeout=300,
                 delete_after_result=True, logger=None):
        self.userid = userid
        self.passwd = passwd
        self.queue_name = queue_name
        if result_format not in self.OUTPUT_FORMATS:
            raise ValueError('Output format must be on of %s' % self.OUTPUT_FORMATS)
        self.result_format = result_format
        self.timeout = timeout
        self.delete_after_result = delete_after_result
        if logger is None:
            raise RuntimeError('logger must be specified')
        self.logger = logger
        # for internal
        self.session = None
        self.isopened = False
        self.key = None
        self.status_code = 0
        self.queue = None
        self.annotation = None
        self.status = None
        self.arrived_at_after = None
        self.arrived_at_before = None
        self.document_url = None
        # open as soon as created
        self.open()

    # ==========================================================================
    def open(self):
        if self.isopened:
            self.close()
        self.session = requests.session()
        self.login()

    # ==========================================================================
    def close(self):
        if self.isopened:
            self.logout()
            self.session.close()
        self.session = None
        self.isopened = False
        self.key = None

    # ==========================================================================
    def __enter__(self):
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    def login(self):
        headers = {
            'Content-Type': 'application/json',
        }
        data = '{"username": "%s", "password": "%s"}' % (self.userid, self.passwd)
        rp = self.session.post('%s/auth/login' % self.V1_API,
                               headers=headers, data=data)
        self.status_code = rp.status_code
        self.logger.debug('after login [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Invalid user or password')
        rd = json.loads(rp.text)
        self.key = rd['key']

    # ==========================================================================
    def get_queue(self):
        if not self.key:
            raise RuntimeError('Login first')
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        params = (
            ('page_size', '1000'),
        )
        rp = self.session.get('%s/queues' % self.V1_API,
                              headers=headers, params=params)
        self.status_code = rp.status_code
        self.logger.debug('after get_queue [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Cannot get available queue')
        rd = json.loads(rp.text)
        if not self.queue_name:
            rq = rd['results'][0]
            self.queue = rq['id']
            self.logger.debug('first queue "%s" selected' % rq['name'])
        else:
            b_found = False
            for rq in rd['results']:
                if rq['name'] == self.queue_name:
                    b_found = True
                    self.queue = rq['id']
                    self.logger.debug('queue "%s" found' % rq['name'])
                    break
            if not b_found:
                rq = rd['results'][0]
                self.queue = rq['id']
                self.logger.debug('first queue "%s" selected (not found)'
                                  % rq['name'])

    # ==========================================================================
    def upload(self, imgfile):
        if not self.key:
            raise RuntimeError('Login first')
        if not os.path.exists(imgfile):
            raise IOError('Image file "%s" not found' % imgfile)
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        files = {
            'content': (os.path.basename(imgfile), open(imgfile, 'rb')),
        }
        self.arrived_at_after = datetime.datetime.now()
        rp = self.session.post('%s/queues/%s/upload' % (self.V1_API, self.queue),
                               headers=headers, files=files)
        self.status_code = rp.status_code
        self.logger.debug('after upload [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Cannot upload image file "%s"' % imgfile)
        rd = json.loads(rp.text)
        anno_str = rd['results'][0]['annotation']
        self.annotation = anno_str.split('/')[-1]

    # ==========================================================================
    def get_status(self):
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        rp = self.session.get('%s/annotations/%s' % (self.V1_API, self.annotation),
                              headers=headers)
        self.status_code = rp.status_code
        # self.logger.debug('after get_status [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Cannot get status')
        rd = json.loads(rp.text)
        if self.status != rd['status']:
            self.logger.info('Status changed into %s' % rd['status'])
            self.status = rd['status']
            if self.status == 'exported':
                self.arrived_at_before = datetime.datetime.now()
        return rd['status']

    # ==========================================================================
    def get_result(self):
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        params = (
            ('format', 'json'),  # self.result_format),
            ('status', 'exported'),
            # ('arrived_at_after', self.arrived_at_after.strftime("%Y-%m-%d %H:%M:%S")),  # 2019-10-13 00:00:00
            # ('arrived_at_before', self.arrived_at_before.strftime("%Y-%m-%d %H:%M:%S")),
            ('id', self.annotation)
        )
        rp = self.session.get('%s/queues/%s/export' % (self.V1_API, self.queue),
                              headers=headers, params=params)
        self.status_code = rp.status_code
        self.logger.debug('after get_result [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Cannot get result')
        # if self.result_format != 'json':
        #     return rp.text
        rd = json.loads(rp.text)
        # noinspection PyBroadException
        try:
            self.document_url = rd['results'][0]['document']['url']
        except Exception:
            self.document_url = None
        if self.result_format == 'json':
            r = rd
        else:
            # get once more for the format except
            headers = {
                'Authorization': 'token %s' % self.key,
            }
            params = (
                ('format', self.result_format),
                ('status', 'exported'),
                # ('arrived_at_after', self.arrived_at_after.strftime("%Y-%m-%d %H:%M:%S")),  # 2019-10-13 00:00:00
                # ('arrived_at_before', self.arrived_at_before.strftime("%Y-%m-%d %H:%M:%S")),
                ('id', self.annotation)
            )
            rp = self.session.get('%s/queues/%s/export' % (self.V1_API, self.queue),
                                  headers=headers, params=params)
            self.status_code = rp.status_code
            self.logger.debug('after get_result [%s]' % self.status_code)
            if rp.status_code // 10 != 20:
                raise RuntimeError('Cannot get result')
            r = rp.text
        if self.delete_after_result and self.document_url:
            self.delete()
        return r

    # ==========================================================================
    def delete(self):
        if not self.document_url:
            raise RuntimeError('Cannot delete document')
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        rp = self.session.delete(self.document_url, headers=headers)
        self.status_code = rp.status_code
        self.logger.debug('after delete [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            # raise RuntimeError('Cannot delete')
            return False
        return True

    # ==========================================================================
    def logout(self):
        headers = {
            'Authorization': 'token %s' % self.key,
        }
        rp = self.session.post('%s/auth/logout' % self.V1_API, headers=headers)
        self.status_code = rp.status_code
        self.logger.debug('after logout [%s]' % self.status_code)
        if rp.status_code // 10 != 20:
            raise RuntimeError('Cannot logout')

    # ==========================================================================
    def extract(self, imgfile):
        if not os.path.exists(imgfile):
            raise IOError('Image file "%s" not found' % imgfile)
        s_ts = datetime.datetime.now()
        self.get_queue()
        self.upload(imgfile)
        while True:
            rs = self.get_status()
            if rs == 'exported':
                break
            time.sleep(2)
            e_ts = datetime.datetime.now()
            ts_delta = e_ts - s_ts
            if ts_delta.total_seconds() >= self.timeout:
                raise TimeoutError('Processing timeout exceed %s seconds'
                                   % self.timeout)
        r = self.get_result()
        if self.result_format == 'json':
            return json.dumps(r)
        elif self.result_format == 'csv':
            # r = r.replace(r'\r\n', r'\n')
            r = re.sub(r'[\r\n]+', r'\n', r)
        return r


################################################################################
@func_log
def do_rossum(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        with RossumApi(argspec.userid, argspec.passwd,
                       queue_name=argspec.qname,
                       result_format=argspec.result_format,
                       timeout=argspec.timeout,
                       delete_after_result=not argspec.keep_doc,
                       logger=mcxt.logger) as ra:
            r = ra.extract(argspec.img_file)
            print(r, end='')
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
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
        group='1',  # AI Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Rossum',
        icon_path=get_icon_path(__file__),
        description='Extract invoice data from PDF using Rossum (https://rossum.ai/)',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--qname',
                          display_name='Queue Name', show_default=True,
                          help='Queue name to process if not specified or found first queue will be used')
        mcxt.add_argument('--timeout', type=int, default=300,
                          display_name='Process Timeout', min_value=1,
                          help='Timeout for waiting to get result. default is [[300]] sec')
        mcxt.add_argument('--keep-doc',
                          display_name='Keep Doc', action='store_true',
                          help='If this flag is set keep in queue')
        # ##################################### for app dependent parameters
        mcxt.add_argument('userid',
                          display_name='User Email',
                          help='Rossum login id (email)')
        mcxt.add_argument('passwd',
                          display_name='User Password', input_method='password',
                          help='Rossum login password')
        mcxt.add_argument('img_file',
                          display_name='Image File', input_method='fileread',
                          help='Imagefile to extract data including pdf')
        mcxt.add_argument('result_format',
                          display_name='Result Format', choices=RossumApi.OUTPUT_FORMATS,
                          default='json',
                          help='Result format after extracting')
        argspec = mcxt.parse_args(args)
        return do_rossum(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
