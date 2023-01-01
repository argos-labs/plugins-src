"""
====================================
 :mod:`argoslabs.api.requests.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/03/25]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/25]
#     - 기존 httpie를 이용한 argoslabs.api.rest 에 제한이 있을 수 있어 requests를
#       바로 이용하도록 함

################################################################################
import os
import sys
import json
import requests
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.api.requests import _main as main
from alabs.common.util.vvencoding import get_file_encoding


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    # cwd = os.getcwd()

    # ==========================================================================
    def setUp(self) -> None:
        cwd = os.path.dirname(os.path.abspath(__file__))
        os.chdir(cwd)

    # ==========================================================================
    def test0000_init(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.assertTrue(os.path.abspath(os.getcwd()) == cwd)

    # ==========================================================================
    def test0100_get_users_page2(self):
        try:
            r = main('GET', '  https://reqres.in/api/users?page=2 ')  # need strip
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_get_user_2(self):
        of = 'foo.txt'
        try:
            r = main('GET', 'https://reqres.in/api/users/2',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                js = json.loads(rs)
            self.assertTrue(js['data']['id'] == 2)

            # call twice on purpose
            r = main('GET', 'https://reqres.in/api/users/2',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['data']['email'])

        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0120_get_user_23_not_found(self):
        of = 'foo.txt'
        try:
            r = main('GET', 'https://reqres.in/api/users/23',
                     '--errfile', of)
            self.assertTrue(r == 4)
            with open(of) as ifp:
                rs = ifp.read()
                self.assertTrue(rs.find('Not Found for url') > 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0130_get_list(self):
        of = 'foo.txt'
        try:
            r = main('GET', 'https://reqres.in/api/unknown',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['total'] == 12 and len(js['data']) >= 3)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0140_get_single(self):
        of = 'foo.txt'
        try:
            r = main('GET', 'https://reqres.in/api/unknown/2',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['data']['id'] == 2 and
                            js['data']['year'] == 2001)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0150_create_user(self):
        of = 'foo.txt'
        try:
            # kwargs = {
            #     'data': {'name': 'morpheue', 'job': 'leader'}
            # }
            # rp = requests.post('https://reqres.in/api/users', **kwargs)
            # print(rp.status_code)
            # print(rp.text)

            r = main('POST', 'https://reqres.in/api/users',
                     '--params', 'name: morpheus',
                     '--params', 'job:leader',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['name'] == 'morpheus' and
                            js['job'] == "leader")
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0160_update_user(self):
        of = 'foo.txt'
        try:
            r = main('PUT', 'https://reqres.in/api/users/2',
                     '--params', 'name:morpheus',
                     '--params', 'job:zion resident',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['name'] == 'morpheus' and
                            js['job'] == "zion resident")
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0170_update_user_patch(self):
        of = 'foo.txt'
        try:
            r = main('PATCH', 'https://reqres.in/api/users/2',
                     '--params', 'name:morpheus',
                     '--params', 'job:my job',  # TODO: 한글을 넣었더니 오류 발생
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['name'] == 'morpheus' and
                            js['job'] == 'my job')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0180_delete_user(self):
        of = 'foo.txt'
        try:
            r = main('DELETE', 'https://reqres.in/api/users/2',
                     '--outfile', of)
            self.assertTrue(r == 0)  # 204 response
            with open(of) as ifp:
                rstr = ifp.read()
                self.assertTrue(not rstr)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0190_register_success(self):
        of = 'foo.txt'
        try:
            r = main('POST', 'https://reqres.in/api/register',
                     '--params', 'email:eve.holt@reqres.in',
                     '--params', 'password:pistol',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['token'] == 'QpwL5tke4Pnpja7X4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0200_register_failure(self):
        of = 'foo.txt'
        try:
            r = main('POST', 'https://reqres.in/api/register',
                     '--params', 'email:mcchae@argos-labs.com',
                     '--outfile', of)
            self.assertTrue(r == 4)  # 400 response
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['error'] == 'Missing password')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0210_login_success(self):
        of = 'foo.txt'
        try:
            r = main('POST', 'https://reqres.in/api/login',
                     '--params', 'email:eve.holt@reqres.in',
                     '--params', 'password:cityslicka',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['token'] == 'QpwL5tke4Pnpja7X4')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0220_login_failure(self):
        of = 'foo.txt'
        try:
            r = main('POST', 'https://reqres.in/api/login',
                     '--params', 'email:mcchae@argos-labs.com',
                     '--outfile', of)
            self.assertTrue(r != 0)  # response 400
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['error'] == 'Missing password')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0230_get_list_with_delay(self):
        of = 'foo.txt'
        try:
            r = main('GET', 'https://reqres.in/api/users?delay=3',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                print(ifp.read())
                ifp.seek(0, 0)
                js = json.load(ifp)
            self.assertTrue(js['total'] == 12 and len(js['data']) >= 3)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0300_ts_api_baemin(self):
    #     of = 'foo.txt'
    #     try:
    #         r = main(
    #             'GET', "https://api.coupangeats.com/endpoint/store.get_clp",
    #             '--params', 'categoryId:2',
    #             '--params', 'nextToken:',
    #             '--params', 'badgeFilters:',

    #             '--headers', 'X-EATS-OS-TYPE: ANDROID',
    #             '--headers', 'X-EATS-ACCESS-TOKEN: 51sig1lT7YNWXgOmfUOqw8EMs_bFEj5995eFtiXBt3VLVPj3gSl7IJkG-k5XUFXIjo_Oibk1gGYSJSY99iCMD02e6IXaa3k_zFdgbXgdHXMPc4kxzICtKEFjv63h-dn2eRtSiw_G2G4lfKZX-aBizEs_uFf5kO0dOTJ_xRC34EyngTuOEzy2QTWyfApNe6GiD-CGSFX6pbSDtwmLj9-C_F18iAk6L5Zae1VzieGYUS3qBE6NzY12QX9j14j0MfQqTAhKVOXCb0Fi5vPGzWRFt2_WV29ouaQa5gjT60JStTM=',
    #             '--headers', 'X-EATS-DEVICE-DENSITY: XXHDPI',
    #             '--headers', 'X-EATS-DEVICE-ID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592',
    #             '--headers', 'X-EATS-NETWORK-TYPE: wifi',
    #             '--headers', 'User-Agent: Android-Coupang-Eats-Customer/1.1.34',
    #             '--headers', 'X-EATS-TIME-ZONE: Asia/Seoul',
    #             '--headers', 'X-EATS-DEVICE-MODEL: SM-G960N',
    #             '--headers', 'X-EATS-APP-VERSION: 1.1.34',
    #             '--headers', 'X-EATS-LOCALE: ko-KR',
    #             '--headers', 'X-EATS-SESSION-ID: d808d2c2-73ff-4326-bd7a-cfe4d4b06cd0',
    #             '--headers', 'X-EATS-RESOLUTION-TYPE: 1080x2076',
    #             '--headers', 'X-EATS-OS-VERSION: 8.0.0',
    #             '--headers', 'X-EATS-PCID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592',
    #             '--headers', 'Accept-Language: ko-KR',
    #             '--headers', 'X-EATS-LOCATION: {"addressId":4404538,"latitude":37.5088318832,"longitude":127.034317309,"zipcode":"06108"}',
    #             # '--headers', "X-EATS-LOCATION: {'addressId':4404538,'latitude':37.5088318832,'longitude':127.034317309,'zipcode':'06108'}",
    #             '--headers', 'Host: api.coupangeats.com',
    #             '--headers', 'Connection: Keep-Alive',
    #             '--headers', 'Accept-Encoding: gzip',
    #             '--outfile', of,
    #         )
    #         self.assertTrue(r == 0)
    #         with open(of, encoding='utf-8') as ifp:
    #             print(ifp.read())
    #             ifp.seek(0, 0)
    #             js = json.load(ifp)
    #         # 2021.03.25 js['data'] is None
    #         # self.assertTrue(len(js['data']['entityList']) > 20)
    #         self.assertTrue('data' in js)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0400_asj572_encoding_error(self):
        of = 'error.txt'
        try:
            # r = main('GET', 'https://google.com')
            r = main('GET', 'https://www.anzen.mofa.go.jp/index.html',
                     '--encoding', 'utf-8',
                     '--outfile', of)  # need strip
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
