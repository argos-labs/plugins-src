"""
====================================
 :mod:`argoslabs.api.rest`
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
# --------
#
#  * [2023/06/26]
#     - python 3.9 버전에서 지원안하는 라이브러리 requirements에서 PySocks, requests-hawk, httpie-jwt-auth 제외
#  * [2022/12/14]
#     - Next contents are not supported because of --file index are deleted
#     - modify help contents for --req-item
#  * [2022/12/01]
#     - delete --file option : latest httpie does not support @@
#  * [2021/08/10]
#     - upload functionality test
#  * [2021/07/07]
#     - get http executable
#  * [2021/03/26]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/23]
#     - add unicode 결과를 utf-8로 변환하여 출력 ('\uc6c3' => '웃')
#  * [2020/12/15]
#     - 기존 #cryptography>=2.8 오류 발생하여, cryptography==3.2 설치하도록 수정
#  * [2020/10/26]
#     - hpof를 삭제하는데 오류 발생. 따라서 시작 시 temp/httpie_*.txt 삭제
#     - PySocks!=1.5.7,>=1.5.6
#  * [2020/04/09]
#     - encoding 문제 해결
#  * [2020/02/17]
#     - requirement.txt에서 httpie 버전을 최신으로 하였더니 (2.x) 오류 발생
#       httpie-aws-auth 가 없으면 오류 안 발생
#  * [2019/12/18]
#     - 실제 테스트 머신에서 httpie가 cryptography>=2.8 요구
#  * [2019/12/04]
#     - return 값을 http[s] response code 를 주었는데 기존 플러그인과 안 맞음
#     - 정상 == 0, 비정상 != 0
#  * [2019/03/15]
#     - --file 옵션의 디폴트가 [] 인 경우 현재 Stu 오류 발생하여 None으로 수정
#  * [2019/03/14]
#     - --file 추가 및 Girish가 요청한 API 테스트 (tests/httpie-test 참고)
#  * [2019/03/13]
#     - --errfile 용 수정
#  * [2019/03/06]
#     - starting test
#  * [2018/11/28]
#     - starting

################################################################################
import os
import re
import sys
import glob
import argparse
import subprocess
import tempfile
# from httpie.core import main as http_main
from alabs.common.util.vvencoding import get_file_encoding
from io import TextIOWrapper
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class CustomFormatter(argparse.HelpFormatter):
    """Custom formatter for setting argparse formatter_class. Identical to the
    default formatter, except that very long option strings are split into two
    lines.
    """
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)
            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append('%s %s' % (option_string, args_string))
            if sum(len(s) for s in parts) < self._width - (len(parts) - 1) * 2:
                return ', '.join(parts)
            else:
                return ',\n  '.join(parts)


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


# def log_error(msg, *args, **kwargs):
#     msg = msg % args
#     level = kwargs.get('level', 'error')
#     #assert level in ['error', 'warning']
#     sys.stderr.write('\nhttp: %s: %s\n' % (level, msg))


################################################################################
def get_http_exec():
    # if sys.platform == 'win32':
    dir_name = os.path.dirname(sys.executable)
    return os.path.join(dir_name, 'http')


################################################################################
# noinspection PyProtectedMember
@func_log
def http_do(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    for f in glob.glob(os.path.join(tempfile._get_default_tempdir(),
                                    'httpie_*.txt')):
        os.remove(f)

    # argument recombine
    hpof = None
    try:
        args = list()
        args.append('--ignore-stdin')
        if argspec.form:
            args.append('--form')
        # in Windows --pretty and --output cannot exists at the same time
        # args.append('--pretty')
        # # args.append(argspec.pretty)
        # args.append('format')
        args.append('--print')
        # args.append(argspec.print)
        args.append('hb')
        # if argspec.stream:
        #     args.append('--stream')
        # if argspec.download:
        #     args.append('--download')
        # if argspec.cont:
        #     args.append('--continue')
        if argspec.session:
            args.append('--session')
            args.append(argspec.session)
        if argspec.session_read_only:
            args.append('--session-read-only')
            args.append(argspec.session_read_only)
        if argspec.auth_type:
            args.append('--auth-type')
            args.append(argspec.auth_type)
        if argspec.auth:
            args.append('--auth')
            args.append(argspec.auth)
        if argspec.proxy:
            for px in argspec.proxy:
                args.append('--proxy')
                args.append(px)
        if argspec.follow:
            args.append('--follow')
        if argspec.verify:
            args.append('--verify')
            args.append(argspec.verify)
        if argspec.ssl:
            args.append('--ssl')
            args.append(argspec.ssl)
        if argspec.cert:
            args.append('--cert')
            args.append(argspec.cert)
        if argspec.cert_key:
            args.append('--cert-key')
            args.append(argspec.cert_key)
        if argspec.timeout > 0:
            args.append('--timeout')
            args.append(str(argspec.timeout))
        # if argspec.traceback:
        #     args.append('--traceback')
        # if argspec.default_scheme:
        #     args.append('--default-scheme')
        #     args.append(argspec.default_scheme)
        # if argspec.debug:
        #     args.append('--debug')
        args.append(argspec.method)
        args.append(argspec.url.strip())
        if argspec.req_item:
            for ri in argspec.req_item:
                # 2019.03.14 --form에서 @@1 (1-based) 을 @foo.img 처럼 치환
                atat = ri.find('@@')
                if atat >= 0:
                    fndx = int(ri[atat+2:])
                    if not (isinstance(argspec.file, list)
                            and 0 < fndx <= len(argspec.file)):
                        raise ArgsError('file index %d needed but length of '
                                        'files list is %d'
                                        % (fndx, len(argspec.file)))
                    fn = argspec.file[fndx-1]
                    if not os.path.exists(fn):
                        raise IOError('--file %s does not exists' % fn)
                    ri = ri[:atat] + '@%s' % fn
                args.append(ri)
        # call HTTPie main
        # http_main(args=args)

        # HTTP response 결과 처리
        # noinspection PyUnresolvedReferences
        hpof = os.path.join(tempfile._get_default_tempdir(),
                            'httpie_%s.txt' % next(tempfile._get_candidate_names()))
        # hpof = 'C:\\work\\%s.txt' % next(tempfile._get_candidate_names())
        args.append('--output')
        args.append(hpof)

        cmds = [get_http_exec()]
        cmds.extend(args)
        stdout = None
        if isinstance(mcxt._stdout, TextIOWrapper):
            stdout = mcxt._stdout
        stderr = None
        if isinstance(mcxt._stderr, TextIOWrapper):
            stderr = mcxt._stderr
        po = subprocess.Popen(cmds, stdout=stdout, stderr=stderr)
        po.wait()
        rc = po.returncode
        encoding = get_file_encoding(hpof)
        with open(hpof, encoding=encoding) as ifp:
            for i, line in enumerate(ifp):
                line = line.strip()
                if i == 0:
                    rc = int(line.split()[1])
                if not line:
                    break
            jsstr = ifp.read()
        if stdout is None:
            stdout = sys.stdout
        if jsstr:
            stdout.write(conv_from_unicode(jsstr))
        mcxt.logger.info('>>>end...')
        r = 0 if rc // 10 == 20 else 1
        return r
    except Exception as e:
        sys.stderr.write('Error: %s' % str(e))
        raise
    # finally:
    #     # 다음 hpof를 삭제하는데 오류 발생. 따라서 시작 시 temp/httpie_*.txt 삭제
    #     if hpof and os.path.exists(hpof):
    #         os.remove(hpof)


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    methods = ['get', 'post', 'put', 'patch', 'delete',
               'GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    with ModuleContext(
        owner='ARGOS-LABS',
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='REST API',
        icon_path=get_icon_path(__file__),
        description='This is a plugin for RESTful API using HTTPie',
        formatter_class=CustomFormatter
    ) as mcxt:
        # ######################################## for app dependent options
        # ----------------------------------------------------------------------
        # mcxt.add_argument('--file', action="append", default=None,
        #                   input_method='fileread',
        #                   help='''file list to use in --req-item for @@index (1-based)''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--req-item', '-i', action="append",
                          display_name='Req Item',
                          help='Request Item at data part as input')
      #                     help='''REQUEST_ITEM
      # Optional key-value pairs to be included in the request. The separator used
      # determines the type:
      #
      # ':' HTTP headers:
      #     Referer:http://httpie.org  Cookie:foo=foo  User-Agent:bacon/1.0
      # '==' URL parameters to be appended to the request URI:
      #     search==httpie
      # '=' Data fields to be serialized into a JSON object (with --json, -j)
      #     or form data (with --form, -f):
      #     name=HTTPie  language=Python  description='CLI HTTP client'
      # ':=' Non-string JSON data fields (only with --json, -j):
      #     awesome:=true  amount:=42  colors:='["red", "green", "blue"]'
      # '@' Form file fields (only with --form, -f):
      #     cs@~/Documents/CV.pdf
      # '=@' A data field like '=', but takes a file path and embeds its content:
      #      essay=@Documents/essay.txt
      # ':=@' A raw JSON field like ':=', but takes a file path and embeds its content:
      #     package:=@./package.json
      #
      # You can use a backslash to escape a colliding separator in the field name:
      #     field-name-with\\:colon=value''')

    # 2022/12/14 : Next contents are not supported because of --file index are deleted
    #   '@@' Form file fields (only with --form, -f): 
    #       index of --file list (1-based)
    #       cs@@1
    #   '=@@' A data field like '=', but takes a file path and embeds its content:
    #       index of --file list (1-based)
    #       essay=@@2
    #   ':=@@' A raw JSON field like ':=', but takes a file path and embeds its content:
    #       package:=@@1


        # ----------------------------------------------------------------------
        mcxt.add_argument('--form', action="store_true",
                          display_name='Form',
                          help='Flag for using form at HTML')
      #                     help="""--form, -f
      # Data items from the command line are serialized as form fields.
      # The Content-Type is set to application/x-www-form-urlencoded (if not
      # specified). The presence of any file fields results in a
      # multipart/form-data request.""")
    #    # ----------------------------------------------------------------------
    #    mcxt.add_argument('--pretty', action="store", default='format',
    #                      choices=['all', 'colors', 'format', 'none'],
    #                      help='''--pretty {all,colors,format,none}
    #  Controls output processing. The value can be "none" to not prettify
    #  the output (default for redirected output), "all" to apply both colors
    #  and formatting (default for terminal output), "colors", or "format".''')
    #    # ----------------------------------------------------------------------
    #    mcxt.add_argument('--print', action="store", default='b',
    #                      help="""--print WHAT, -p WHAT
    # String specifying what the output should contain:
    #      'H' request headers
    #      'B' request body
    #      'h' response headers
    #      'b' response body
    #  The default behaviour is 'b' (i.e., only the response body
    #  is printed), if standard output is not redirected. If the output is piped
    #  to another program or to a file, then only the response body is printed
    #  by default.""")
    #   # ----------------------------------------------------------------------
    #   mcxt.add_argument('--stream', '-S', action="store_true",
    #                     help="""--stream, -S
    # Always stream the output by line, i.e., behave like `tail -f'.
    #
    # Without --stream and with --pretty (either set or implied),
    # HTTPie fetches the whole response before it outputs the processed data.
    #
    # Set this option when you want to continuously display a prettified
    # long-lived response, such as one from the Twitter streaming API.
    #
    # It is useful also without --pretty: It ensures that the output is flushed
    # more often and in smaller chunks.""")
    #   # ----------------------------------------------------------------------
    #   mcxt.add_argument('--download', '-d', action="store_true",
    #                     help="""--download, -d
    # Do not print the response body to stdout. Rather, download it and store it
    # in a file. The filename is guessed unless specified with --output
    # [filename]. This action is similar to the default behaviour of wget.""")
    #   # ----------------------------------------------------------------------
    #   mcxt.add_argument('--continue', '-c', dest='cont',
    #                     action="store_true",
    #                     help="""--continue, -c
    # Resume an interrupted download. Note that the --output option needs to be
    # specified as well.""")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--session', action="store", default=None,
                          display_name='Session',
                          help='Session name or path')
      #                     help='''--session SESSION_NAME_OR_PATH
      # Create, or reuse and update a session. Within a session, custom headers,
      # auth credential, as well as any cookies sent by the server persist between
      # requests.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--session-read-only', action="store", default=None,
                          display_name='Session ReadOnly',
                          help='Readonly ession name or path')
      #                     help='''--session-read-only SESSION_NAME_OR_PATH
      # Create or read a session without updating it form the request/response
      # exchange.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--auth-type', action="store", nargs='?',
                          display_name='Auth Type',
                          default=None,
                          choices=['api-auth', 'aws', 'basic', 'digest',
                                   'edgegrid', 'hawk', 'hmac', 'jwt',
                                   'negotiate', 'ntlm', 'oauth1'],
                          help='Refer https://httpie.io/docs/cli/auth-plugins')
      #                     help='''--auth-type {api-auth,aws,basic,digest,edgegrid,hawk,hmac,jwt,negotiate,ntlm,oauth1},
      # -A {api-auth,aws,basic,digest,edgegrid,hawk,hmac,jwt,negotiate,ntlm,oauth1}
      # The authentication mechanism to be used. Defaults to "basic".
      #
      # "basic": Basic HTTP auth
      # "digest": Digest HTTP auth
      # "hawk": Hawk Auth (provided by https://github.com/mozilla-services/requests-hawk)
      # "oauth1": OAuth 1.0a 2-legged (provided by https://github.com/httpie/httpie-oauth)
      # "ntlm": NTLM auth (provided by https://github.com/httpie/httpie-ntlm)
      # "negotiate": SPNEGO auth (provided by https://github.com/ndzou/httpie-negotiate)
      # "jwt": JWT auth (provided by https://github.com/teracyhq/httpie-jwt-auth)
      #   Set the right format for JWT auth request
      # "hmac": HMAC token auth (provided by https://github.com/guardian/httpie-hmac-auth)
      #   Sign requests using a HMAC authentication method like AWS
      # "edgegrid": EdgeGrid auth (provided by https://github.com/akamai/httpie-edgegrid)
      # "aws": AWS auth (provided by https://github.com/httpie/httpie-aws-auth)
      # "api-auth": ApiAuth auth (provided by https://github.com/pd/httpie-api-auth)
      #   Sign requests using the ApiAuth authentication method''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--auth', '-a', action="store", nargs='?',
                          display_name='Auth',
                          default=None,
                          help='''--auth USER[:PASS], -a USER[:PASS]
      If only the username is provided (-a username), HTTPie will prompt
      for the password.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--proxy', action="append",
                          display_name='Proxy',
                          help='''--proxy PROTOCOL:PROXY_URL
      String mapping protocol to the URL of the proxy
      (e.g. http:http://foo.bar:3128). You can specify multiple proxies with
      different protocols.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--follow', '-F', action="store_true",
                          display_name='Follow',
                          help='''--follow, -F
      Follow 30x Location redirects.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--verify', action="store", nargs='?', default=None,
                          display_name='Verify',
                          choices=['yes', 'no', 'true', 'false'],
                          help='''--verify VERIFY
      Set to "no" (or "false") to skip checking the host's SSL certificate.
      Defaults to "yes" ("true"). You can also pass the path to a CA_BUNDLE file
      for private certs. (Or you can set the REQUESTS_CA_BUNDLE environment
      variable instead.)''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--ssl', action="store", nargs='?', default=None,
                          display_name='SSL',
                          choices=['ssl2.3', 'tls1', 'tls1.1', 'tls1.2'],
                          help="""--ssl {ssl2.3,tls1,tls1.1,tls1.2}
      The desired protocol version to use. This will default to
      SSL v2.3 which will negotiate the highest protocol that both
      the server and your installation of OpenSSL support. Available protocols
      may vary depending on OpenSSL installation (only the supported ones
      are shown here).""")
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cert', action="store", default=None,
                          display_name='Cert',
                          help='''--cert CERT
      You can specify a local cert to use as client side SSL certificate.v
      This file may either contain both private key and certificate or you may
      specify --cert-key separately.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--cert-key', action="store", default=None,
                          display_name='Cert Key',
                          help='''--cert-key CERT_KEY
      The private key to use with SSL. Only needed if --cert is given and the
      certificate file does not contain the private key.''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--timeout', type=int, action="store", default=30,
                          display_name='Timeout',
                          help='''--timeout SECONDS
      The connection timeout of the request in seconds. The default value is
      30 seconds''')

        #   # ----------------------------------------------------------------------
        #   mcxt.add_argument('--traceback', action="store_true",
        #                     help='''--traceback
        # Prints the exception traceback should one occur.''')
        #   # ----------------------------------------------------------------------
        #   mcxt.add_argument('--default-scheme', action="store",
        #                     help='''--default-scheme DEFAULT_SCHEME
        # The default scheme to use if not specified in the URL.''')
        #   # ----------------------------------------------------------------------
        #   mcxt.add_argument('--debug', action="store_true",
        #                     help='''--debug
        # Prints the exception traceback should one occur, as well as other
        # information useful for debugging HTTPie itself and for reporting bugs.''')
        # ##################################### for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('method', choices=methods, default='get',
                          display_name='Method',
                          help='''METHOD
      The HTTP method to be used for the request (GET, POST, PUT, DELETE, ...).

      This argument can be omitted in which case HTTPie will use POST if there
      is some data to be sent, otherwise GET:''')
        # ----------------------------------------------------------------------
        mcxt.add_argument('url',
                          display_name='URL',
                          help='HTTP URL to call RESTful API')
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
