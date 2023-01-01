"""
====================================
 :mod:`argoslabs.python.case`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for "Case Decision"
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/09/29]
#     - "Expression" 패러미터에 input_method='base64' 지정 및 디코딩
#       <== PAM에서 문제가 발생하여 결국 PAM에서 수정하기로 하고 원복
#  * [2021/09/16]
#     - return '0' else case
#  * [2021/09/14]
#     - starting

################################################################################
import os
import re
import sys
import traceback
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path  # , vv_base64_decode


################################################################################
def vv_base64_decode(v):
    return v


################################################################################
REC = re.compile(r'\s*(==|!=|<>|>=|<=|\|\||=|>|<)\s*')
REC_N = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")


################################################################################
def get_safe_operend(opr):
    # 우선 앞뒤 공백 제거
    opr = opr.strip()
    m = REC_N.match(opr)
    if m is not None:
        return 'numeric', opr
    if opr:
        if opr[0] == opr[-1] == "'":
            opr[0] = opr[-1] = '"'
        if opr[0] == opr[-1] == '"':
            return 'str', opr
    return 'str', f'"{opr}"'


################################################################################
def get_safe_op(op):
    if op in ('==', '='):
        return '=='
    elif op in ('!=', '<>'):
        return '!='
    elif op in ('>', '>=', '<', "<=", '||'):
        return op
    raise ValueError(f'Invalid operator "{op}"')


################################################################################
def do_wildcard_match(left, right):
    # left must be literal and right must have wildcard
    l = left[1][1:-1] if left[0] == 'str' else left[1]
    r = right[1][1:-1] if right[0] == 'str' else right[1]
    if r.find('*') < 0:
        raise ValueError('Right operand must have Wildcard')
    lit = l
    re_s = r.replace('*', '.*')
    if re_s[0] != '*':
        re_s = '^' + re_s
    if re_s[-1] != '*':
        re_s = re_s + '$'
    m = re.search(re_s, lit)
    if m is not None:
        return True
    return False


################################################################################
def do_safe_eval(exp):
    m = REC.search(exp)
    if m is not None:
        op = get_safe_op(m.groups(1)[0])
        left = get_safe_operend(exp[:m.start(1)])
        right = get_safe_operend(exp[m.end(1):])
        if left[0] == right[0] == 'numeric':
            exp = f'{left[1]} {op} {right[1]}'
        else:
            if op == '||':
                return do_wildcard_match(left, right)
            exp = f'"{left[1]}"' if left[0] == 'numeric' else left[1]
            exp += f' {op} '
            ropr = f'"{right[1]}"' if right[0] == 'numeric' else right[1]
            exp += ropr
        return eval(exp)
    raise ValueError(f'Invalid Expression "{exp}"')


################################################################################
@func_log
def do_case_decision(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.exps:
            raise IOError(f'Cannot get Expressions')
        res_list = list()
        for i, exp in enumerate(argspec.exps):
            exp = vv_base64_decode(exp)
            r = do_safe_eval(exp)
            if r:
                res_list.append(f'{i+1}')
        if res_list:
            print(','.join(res_list), end='')
        else:
            print('0', end='')
        return 0
    except Exception as e:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        msg = '%s\n' % ''.join(_out)
        mcxt.logger.error(msg)
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write(msg)
        return 99
    finally:
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
        group='1002',  # Verifications
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Case Decision',
        icon_path=get_icon_path(__file__),
        description='Execute dynamic python script with 3-rd party modules',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('exps',
                          display_name='Expression',
                          input_method='base64',
                          nargs='+',
                          help='Expession to evaluate')
        # ##################################### for app dependent options
        # mcxt.add_argument('--encoding',
        #                   display_name='Encoding', default='utf-8',
        #                   help='Encoding for script and requirements file, default is [[utf-8]]')
        argspec = mcxt.parse_args(args)
        return do_case_decision(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
