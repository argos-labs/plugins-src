#!/usr/bin/env python
# coding=utf8


"""
====================================
 :mod:`argoslabs.api.graphql`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
GraphQL API

"""
# Authors
# ===========
#
# * Arun Kumar , Jerry
#
# Change Log
# --------
#
#  * [2022/08/01]
#   - upgrated with request

################################################################################
import os
import sys
import json
import requests
import re
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

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


# ################################################################################
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
def conv_query(que,var=None):
    data = {'query': que, 'variables': var}
    encode_query_str = json.dumps(data).encode('utf-8')
    return encode_query_str


################################################################################
@func_log
def start_gql(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:

        if not argspec.url:
            msg = str("URL required")
            mcxt.logger.error(msg)
            sys.stderr.write('%s%s' % (msg, os.linesep))
            return 11
        if not argspec.query:
            msg = str("query required")
            mcxt.logger.error(msg)
            sys.stderr.write('%s%s' % (msg, os.linesep))
            return 11
        ########################################################################
        kwargs = {}
        if argspec.headers:
            kwargs['headers'] = get_safe_dict(argspec.headers)

        if argspec.cookies:
            kwargs['cookies'] = get_safe_dict(argspec.cookies)
        if argspec.variables:
            kwargs['data'] = conv_query(argspec.query,argspec.variables)
        else:
            kwargs['data'] = conv_query(argspec.query)
        url = argspec.url
        rp = requests.post(url, **kwargs,timeout=argspec.timeout)
        if rp.status_code // 10 != 20:
            print(conv_from_unicode(rp.text), end='')
            rp.raise_for_status()
        print(rp.text, end='')

        mcxt.logger.info('>>>end...')
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
        return 9
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
        display_name='GraphQL API',
        icon_path=get_icon_path(__file__),
        description='API Module',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('url', display_name='URI',
                          help='URI graphql server')

        # ----------------------------------------------------------------------
        mcxt.add_argument('query', display_name='Query',
                          help='Query to graphql server')

        # ##################################### for app optional parameters

        mcxt.add_argument('--variables',
                          display_name='Variables',
                          default=None,
                          help='Variables for graphql server, default is None')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--headers', action="append",
                          display_name='Headers',
                          help='HEADER Items like "Content-Type: application/json; charset=utf-8')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cookies', action="append",
                          display_name='Cookies',
                          help='Cookie Items like "session_id: sorryidontcare"')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timeout',
                          display_name='Timeout',
                          type=int, default=10,
                          help='Timeout seconds, default is [[10]]')
        argspec = mcxt.parse_args(args)
        return start_gql(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
