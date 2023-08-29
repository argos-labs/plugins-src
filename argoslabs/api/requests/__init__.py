"""
====================================
 :mod:`argoslabs.api.requests`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# ----------
#
#  * [2022/01/24] Kyobong An
#     - encoding 추가
#  * [2021/03/25]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/25]
#     - 기존 httpie를 이용한 argoslabs.api.rest 에 제한이 있을 수 있어 requests를
#       바로 이용하도록 함

################################################################################
import os
import re
import sys
import json
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

################################################################################
METHODS = {
    'GET': requests.get,
    'POST': requests.post,
    'PUT': requests.put,
    'PATCH': requests.patch,
    'DELETE': requests.delete,
    'HEAD': requests.head,
    'OPTIONS': requests.options,
}


################################################################################
def get_safe_dict(items):
    if not isinstance(items, list):
        return None
    rd = {}
    for item in items:
        k, v = item.split(':', maxsplit=1)
        k = k.strip()
        v = v.strip()
        rd[k] = v
    return rd


################################################################################
def conv_from_unicode(s, target_enc='utf-8'):
    sl = list()
    p_sp = 0
    for m in re.finditer(r'\\u[0-9a-f]{4}', s, re.IGNORECASE):
        # print(f'"{m.group(0)}" {m.start(0)}-{m.end(0)}')
        c_sp, c_ep = m.start(0), m.end(0)
        if p_sp < c_sp:
            sl.append(s[p_sp:c_sp])
        c = eval(f"u'{m.group(0)}'")
        sl.append(c.encode().decode(target_enc))
        p_sp = c_ep
    if not sl:
        return s
    return ''.join(sl)


################################################################################
# noinspection PyProtectedMember
@func_log
def http_do(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    rp = None
    ufopen = None
    try:
        if argspec.method not in METHODS.keys():
            raise ReferenceError(f'Invalid Method "{argspec.method}"')
        if not argspec.url:
            raise ValueError(f'Invalid URL')
        url = argspec.url.strip()
        method_f = METHODS[argspec.method]
        kwargs = {}
        if argspec.headers:
            kwargs['headers'] = get_safe_dict(argspec.headers)
        if argspec.cookies:
            kwargs['cookies'] = get_safe_dict(argspec.cookies)
        if argspec.params:
            if argspec.method == 'GET':
                kwargs['params'] = get_safe_dict(argspec.params)
            else:
                kwargs['data'] = get_safe_dict(argspec.params)
        json_data = None
        if argspec.json_data_file and os.path.exists(argspec.json_data_file):
            with open(argspec.json_data_file, encoding=argspec.encoding) as ifp:
                json_data = json.load(ifp)
        elif argspec.json_data:
            json_data = json.loads(argspec.json_data)
        if json_data:
            kwargs['json'] = json_data

        # 2023.04.12 add
        if argspec.upload_file:
            ufopen = open(argspec.upload_file, 'rb')
            kwargs['files'] = {
                argspec.upload_file_key: ufopen,
            }
            if argspec.token:
                kwargs['files']['token'] = (None, argspec.token)
        if argspec.no_verify:
            kwargs['verify'] = False
        if argspec.cert_file:
            kwargs['cert'] = argspec.cert_file
        if argspec.basic_auth_user or argspec.basic_auth_pass:
            if not (argspec.basic_auth_user and argspec.basic_auth_pass):
                raise ValueError('Invalid "Auth User" or "Auth Pass"')
            kwargs['auth'] = (argspec.basic_auth_user, argspec.basic_auth_pass)

        # Actual call
        rp = method_f(url, **kwargs, timeout=argspec.timeout)
        if argspec.encoding:
            rp.encoding = argspec.encoding
        if rp.status_code // 10 != 20:
            print(conv_from_unicode(rp.text), end='')
            rp.raise_for_status()
        print(rp.text, end='')
        return 0
    except requests.exceptions.HTTPError as e:
        msg = f'HTTP Response Error: {str(e)}'
        sys.stderr.write(msg)
        mcxt.logger.error(msg)
        return rp.status_code // 100
    except Exception as e:
        msg = f'Error: {str(e)}'
        sys.stderr.write(msg)
        mcxt.logger.error(msg)
        return 99
    finally:
        mcxt.logger.info('>>>ended!')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='API Requests',
        icon_path=get_icon_path(__file__),
        description='This is a plugin for RESTful API using python requests module',
    ) as mcxt:

        # ##################################### for app dependent parameters
        mcxt.add_argument('method',
                          display_name='HTTP Method',
                          choices=list(METHODS.keys()),
                          default='GET',
                          help='HTTP[S] methods')
        mcxt.add_argument('url',
                          display_name='URL',
                          help='HTTP[S] URL')

        # ######################################## for app dependent options
        mcxt.add_argument('--params', action="append",
                          display_name='Parameters',
                          help='Parameter Items like "key: value')
        mcxt.add_argument('--headers', action="append",
                          display_name='Headers',
                          help='HEADER Items like "Content-Type: application/json; charset=utf-8')
        mcxt.add_argument('--cookies', action="append",
                          display_name='Cookies',
                          help='Cookie Items like "session_id: sorryidontcare"')
        mcxt.add_argument('--json-data',
                          display_name='JSON data',
                          help='JSON Data, json.dumps string')
        mcxt.add_argument('--json-data-file',
                          display_name='JSON data file',
                          input_method='fileread',
                          help='JSON Data file')
        mcxt.add_argument('--upload-file-key',
                          display_name='Upload Key',
                          default='files',
                          help='Upload file key, default is [[files]]')
        mcxt.add_argument('--upload-file',
                          display_name='Upload File',
                          input_method='fileread',
                          help='Upload file')
        mcxt.add_argument('--token',
                          display_name='Token',
                          help='Token for upload file')
        mcxt.add_argument('--no-verify', action = 'store_true',
                          display_name='No Verify',
                          help='If this flag is set then do not verify SSL')
        mcxt.add_argument('--cert-file',
                          display_name='Cert File',
                          input_method='fileread',
                          help='Cert file')
        mcxt.add_argument('--basic-auth-user',
                          display_name='Auth User',
                          help='Basic auth userid')
        mcxt.add_argument('--basic-auth-pass',
                          display_name='Auth Pass',
                          input_method='password',
                          help='Basic auth password')
        mcxt.add_argument('--encoding',
                          display_name='Encoding',
                          help='Encoding for JSON Data file, Default is [[utf-8]]')
        mcxt.add_argument('--timeout',
                          display_name='Timeout',
                          type=int, default=10,
                          help='Timeout seconds, default is [[10]]')
        argspec = mcxt.parse_args(args)
        return http_do(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
