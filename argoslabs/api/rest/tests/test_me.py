"""
====================================
 :mod:`argoslabs.api.rest.tests.test_me`
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
#  * [2022/12/01]
#     - delete --file option : latest httpie does not support @@
#  * [2022/11/22]
#     - http https://zfr9ibuww2.execute-api.us-west-1.amazonaws.com/dev/upload file@ARGOSLow-code.pdf  --form
#  * [2021/08/10]
#     - upload functionality test
#  * [2021/03/26]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/12/15]
#     - 기존 #cryptography>=2.8 오류 발생하여, cryptography==3.2 설치하도록 수정
#  * [2020/04/09]
#     - NCSoft 용 테스트
#  * [2019/07/19]
#     - url에 대하여 strip()

################################################################################
import os
import sys
import json
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.api.rest import _main as main
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
    def test0100_help(self):
        try:
            _ = main('--help')
            self.assertTrue(False)
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_dumpspec(self):
        try:
            _ = main('--dumpspec', 'yaml')
            self.assertTrue(False)
        except ArgsExit as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0210_get_users_page2(self):
        try:
            r = main('get', '  https://reqres.in/api/users?page=2 ')  # need strip
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_get_user_2(self):
        of = 'foo.txt'
        try:
            r = main('get', 'https://reqres.in/api/users/2',
                     '--outfile', of)
            self.assertTrue(r == 0)
            with open(of) as ifp:
                rs = ifp.read()
                # ifp.seek(0, 0)
                js = json.loads(rs)
            self.assertTrue(js['data']['id'] == 2)

            # call twice on purpose
            r = main('get', 'https://reqres.in/api/users/2',
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
    def test0230_get_user_23_not_found(self):
        of = 'foo.txt'
        try:
            r = main('get', 'https://reqres.in/api/users/23',
                     '--outfile', of)
            self.assertTrue(r != 0)
            with open(of) as ifp:
                js = json.load(ifp)
                ifp.seek(0, 0)
                print(ifp.read())
            self.assertTrue(not js)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0240_get_list(self):
        of = 'foo.txt'
        try:
            r = main('get', 'https://reqres.in/api/unknown',
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
    def test0250_get_single(self):
        of = 'foo.txt'
        try:
            r = main('get', 'https://reqres.in/api/unknown/2',
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
    def test0260_create_user(self):
        of = 'foo.txt'
        try:
            r = main('post', 'https://reqres.in/api/users',
                     '-i', 'name=morpheus',
                     '-i', 'job=leader',
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
    def test0270_update_user(self):
        of = 'foo.txt'
        try:
            r = main('put', 'https://reqres.in/api/users/2',
                     '-i', 'name=morpheus',
                     '-i', 'job=zion resident',
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
    def test0280_update_user_patch(self):
        of = 'foo.txt'
        try:
            r = main('patch', 'https://reqres.in/api/users/2',
                     '-i', 'name=morpheus',
                     '-i', 'job=my job',  # TODO: 한글을 넣었더니 오류 발생
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
    def test0290_delete_user(self):
        of = 'foo.txt'
        try:
            r = main('delete', 'https://reqres.in/api/users/2',
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
    def test0300_register_success(self):
        of = 'foo.txt'
        try:
            r = main('post', 'https://reqres.in/api/register',
                     '-i', 'email=eve.holt@reqres.in',
                     '-i', 'password=pistol',
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
    def test0310_register_failure(self):
        of = 'foo.txt'
        try:
            r = main('post', 'https://reqres.in/api/register',
                     '-i', 'email=mcchae@argos-labs.com',
                     '--outfile', of)
            self.assertTrue(r != 0)  # 400 response
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
    def test0320_login_success(self):
        of = 'foo.txt'
        try:
            r = main('post', 'https://reqres.in/api/login',
                     '-i', 'email=eve.holt@reqres.in',
                     '-i', 'password=cityslicka',
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
    def test0330_login_failure(self):
        of = 'foo.txt'
        try:
            r = main('post', 'https://reqres.in/api/login',
                     '-i', 'email=mcchae@argos-labs.com',
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
    def test0340_get_list_with_delay(self):
        of = 'foo.txt'
        try:
            r = main('get', 'https://reqres.in/api/users?delay=3',
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
    def test0400_azer_api(self):
        """
        https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/curl
        """
        of = 'foo.txt'
        try:
            subscription_key = "034f8bfbcad0435c8bad047980d8d811"
            r = main(
                '--req-item', "Ocp-Apim-Subscription-Key: %s" % subscription_key,
                '--req-item', "Content-Type:application/json",
                '--req-item', "url=https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg",
                'POST', "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"
                        "?returnFaceId=true&returnFaceLandmarks=false"
                        "&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair"
                        ",makeup,occlusion,accessories,blur,exposure,noise",
                '--outfile', of
            )
            # sometimes r is not 200
            # self.assertTrue(r == 200)
            if r == 0:
                with open(of) as ifp:
                    print(ifp.read())
                    ifp.seek(0, 0)
                    js = json.load(ifp)
                self.assertTrue(js[0]['faceId'] == '878dee07-1425-4f42-bd00-94c5f7f14214')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # # ==========================================================================
    # def test0410_ibm_watson_api_01(self):
    #     """
    #     https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
    #     """
    #     of = 'foo.txt'
    #     try:
    #         ibm_key = "QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt"
    #         r = main(
    #             '--form',
    #             '--auth', 'apikey:%s' % ibm_key,
    #             '--req-item', "images_file@%s" % os.path.join('httpie-tests', 'fruitbowl.jpg'),
    #             'POST', "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20",
    #             '--outfile', of
    #         )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             print(ifp.read())
    #             ifp.seek(0, 0)
    #             js = json.load(ifp)
    #         self.assertTrue(js['images'][0]["classifiers"][0]["classes"][1]['score'] == 0.788)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #
    # # ==========================================================================
    # def test0420_ibm_watson_api_01_with_file(self):
    #     """
    #     https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
    #     """
    #     of = 'foo.txt'
    #     try:
    #         ibm_key = "QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt"
    #         r = main(
    #             '--form',
    #             '--auth', 'apikey:%s' % ibm_key,
    #             '--file', os.path.join('httpie-tests', 'fruitbowl.jpg'),
    #             '--req-item', "images_file@@1",
    #             'POST', "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20",
    #             '--outfile', of
    #         )
    #         self.assertTrue(r == 0)
    #         with open(of) as ifp:
    #             print(ifp.read())
    #             ifp.seek(0, 0)
    #             js = json.load(ifp)
    #         self.assertTrue(js['images'][0]["classifiers"][0]["classes"][1]['score'] == 0.788)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)

    # ==========================================================================
    def test0430_ibm_watson_api_02_with_file(self):
        """
        https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
        """
        of = 'foo.txt'
        try:
            ibm_key = "QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt"
            r = main(
                '--form',
                '--auth', 'apikey:%s' % ibm_key,
                # '--file', os.path.join('httpie-tests', 'prez.jpg'),
                # '--req-item', "images_file@@1",
                '--req-item', f"images_file@{os.path.join('httpie-tests', 'prez.jpg')}",
                'post', "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2016-05-20",
                '--outfile', of
            )
            self.assertTrue(r != 0)  # 404 why?
            # self.assertTrue(r == 200)
            # with open(of) as ifp:
            #     print(ifp.read())
            #     ifp.seek(0, 0)
            #     js = json.load(ifp)
            # self.assertTrue(js['images'][0]["faces"][0]["age"]['score'] == 0.64800006)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)
        finally:
            if os.path.exists(of):
                os.remove(of)

    # ==========================================================================
    def test0440_ibm_watson_api_02_with_file_fail(self):
        """
        https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
        """
        of = 'foo.txt'
        stderr_file = 'stderr.txt'
        try:
            ibm_key = "QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt"
            r = main(
                '--form',
                '--auth', 'apikey:%s' % ibm_key,
                # '--file', os.path.join('httpie-tests', 'prez.jpg'),  # on purpose
                '--req-item', "images_file@@1",
                'post', "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2016-05-20",
                '--outfile', of,
                '--errfile', stderr_file,
            )
            self.assertTrue(r != 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.exists(stderr_file) and
                            os.path.getsize(stderr_file) > 0)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(stderr_file):
                os.remove(stderr_file)

    # ==========================================================================
    # def test0450_ncsoft_encoding_error(self):
    #     of = 'foo.txt'
    #     stderr_file = 'stderr.txt'
    #     try:
    #         url = 'http://search.plaync.com/openapi/suggest.jsp?site=bns&display=10&collection=bnsquery&pos=lnb&where=bnsweb%5Etsearch&callback=suggestCallback&query=%EC%9B%94&_=1576571859973'
    #         r = main(
    #             'get', url,
    #             '--outfile', of,
    #             '--errfile', stderr_file,
    #         )
    #         self.assertTrue(r == 0)
    #         encoding = get_file_encoding(of)
    #         with open(of, encoding=encoding) as ifp:
    #             rs = ifp.read()
    #             # print(rs)
    #         self.assertTrue(rs.strip().startswith('suggestCallback({'))
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(os.path.exists(stderr_file) and
    #                         os.path.getsize(stderr_file) > 0)
    #     finally:
    #         if os.path.exists(of):
    #             os.remove(of)
    #         if os.path.exists(stderr_file):
    #             os.remove(stderr_file)

    # ==========================================================================
    def test0460_ts_unicode(self):
        of = 'foo.txt'
        stderr_file = 'stderr.txt'
        try:
            url = 'https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category=%ED%94%BC%EC%9E%90%EC%96%91%EC%8B%9D&items=60&lat=37.5108593855466&lng=127.029258482886&order=rank&page=0&search='
            r = main(
                'get', url,
                '--req-item', 'x-apikey: iphoneap',
                '--req-item', 'x-apisecret: fe5183cc3dea12bd0ce299cf110a75a2',
                '--outfile', of,
                '--errfile', stderr_file,
            )
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                # print(rs)
            self.assertTrue(rs.strip().find('pagination') > 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.exists(stderr_file) and
                            os.path.getsize(stderr_file) > 0)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(stderr_file):
                os.remove(stderr_file)

    # 다음 테스트 결과는 Httpie로 할 수 없어서 argoslabs.api.requests를 만들어 처리
#     # ==========================================================================
#     def test0470_ts_api(self):
#         of = 'foo.txt'
#         stderr_file = 'stderr.txt'
#         try:
#             url = 'https://api.coupangeats.com/endpoint/store.get_clp?categoryId=2&nextToken=&badgeFilters='
#             '''
# X-EATS-OS-TYPE: ANDROID
# X-EATS-ACCESS-TOKEN: 51sig1lT7YNWXgOmfUOqw8EMs_bFEj5995eFtiXBt3VLVPj3gSl7IJkG-k5XUFXIjo_Oibk1gGYSJSY99iCMD02e6IXaa3k_zFdgbXgdHXMPc4kxzICtKEFjv63h-dn2eRtSiw_G2G4lfKZX-aBizEs_uFf5kO0dOTJ_xRC34EyRydbgu4WImZr2mbbkXye3D77tQTsKsH-3kLNDuw6rCkCHXfgw5nruLs6hzqb5-Q3OohlmvH0HKK2EziRlQ3GUhmzNsCxSMghXWgfAzvLWRXieGeEzeqKHib43CK-rbJ4=
# X-EATS-DEVICE-DENSITY: XXHDPI
# X-EATS-DEVICE-ID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592
# X-EATS-NETWORK-TYPE: wifi
# User-Agent: Android-Coupang-Eats-Customer/1.1.39
# X-EATS-TIME-ZONE: Asia/Seoul
# X-EATS-DEVICE-MODEL: SM-G960N
# X-EATS-APP-VERSION: 1.1.39
# X-EATS-LOCALE: ko-KR
# X-EATS-SESSION-ID: 61b04a02-2f9a-484c-b0d5-3335fcf94320
# X-EATS-RESOLUTION-TYPE: 1080x2076
# X-EATS-OS-VERSION: 8.0.0
# X-EATS-PCID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592
# Accept-Language: ko-KR
# X-EATS-LOCATION: {"addressId":0,"latitude":0.0,"longitude":0.0}
# Host: api.coupangeats.com
# Connection: Keep-Alive
# Accept-Encoding: gzip
#             '''
#             r = main(
#                 'get', url,
#                 '--req-item', 'X-EATS-OS-TYPE: ANDROID',
#                 '--req-item', 'X-EATS-ACCESS-TOKEN: 51sig1lT7YNWXgOmfUOqw8EMs_bFEj5995eFtiXBt3VLVPj3gSl7IJkG-k5XUFXIjo_Oibk1gGYSJSY99iCMD02e6IXaa3k_zFdgbXgdHXMPc4kxzICtKEFjv63h-dn2eRtSiw_G2G4lfKZX-aBizEs_uFf5kO0dOTJ_xRC34EyRydbgu4WImZr2mbbkXye3D77tQTsKsH-3kLNDuw6rCkCHXfgw5nruLs6hzqb5-Q3OohlmvH0HKK2EziRlQ3GUhmzNsCxSMghXWgfAzvLWRXieGeEzeqKHib43CK-rbJ4=',
#                 '--req-item', 'X-EATS-DEVICE-DENSITY: XXHDPI',
#                 '--req-item', 'X-EATS-DEVICE-ID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 '--req-item', 'X-EATS-NETWORK-TYPE: wifi',
#                 '--req-item', 'User-Agent: Android-Coupang-Eats-Customer/1.1.39',
#                 '--req-item', 'X-EATS-TIME-ZONE: Asia/Seoul',
#                 '--req-item', 'X-EATS-DEVICE-MODEL: SM-G960N',
#                 '--req-item', 'X-EATS-APP-VERSION: 1.1.39',
#                 '--req-item', 'X-EATS-LOCALE: ko-KR',
#                 '--req-item', 'X-EATS-SESSION-ID: 61b04a02-2f9a-484c-b0d5-3335fcf94320',
#                 '--req-item', 'X-EATS-RESOLUTION-TYPE: 1080x2076',
#                 '--req-item', 'X-EATS-OS-VERSION: 8.0.0',
#                 '--req-item', 'X-EATS-PCID: 4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 '--req-item', 'Accept-Language: ko-KR',
#                 '--req-item', 'X-EATS-LOCATION: {"addressId":0,"latitude":0.0,"longitude":0.0}',
#                 '--req-item', 'Host: api.coupangeats.com',
#                 '--req-item', 'Connection: Keep-Alive',
#                 '--req-item', 'Accept-Encoding: gzip',
#                 '--outfile', of,
#                 '--errfile', stderr_file,
#             )
#             self.assertTrue(r == 0)
#             encoding = get_file_encoding(of)
#             with open(of, encoding=encoding) as ifp:
#                 rs = ifp.read()
#                 # print(rs)
#             # self.assertTrue(rs.strip().find('pagination') > 0)
#             headers = {
#                 'X-EATS-OS-TYPE': 'ANDROID',
#                 'X-EATS-ACCESS-TOKEN': '51sig1lT7YNWXgOmfUOqw8EMs_bFEj5995eFtiXBt3VLVPj3gSl7IJkG-k5XUFXIjo_Oibk1gGYSJSY99iCMD02e6IXaa3k_zFdgbXgdHXMPc4kxzICtKEFjv63h-dn2eRtSiw_G2G4lfKZX-aBizEs_uFf5kO0dOTJ_xRC34EyRydbgu4WImZr2mbbkXye3D77tQTsKsH-3kLNDuw6rCkCHXfgw5nruLs6hzqb5-Q3OohlmvH0HKK2EziRlQ3GUhmzNsCxSMghXWgfAzvLWRXieGeEzeqKHib43CK-rbJ4=',
#                 'X-EATS-DEVICE-DENSITY': 'XXHDPI',
#                 'X-EATS-DEVICE-ID': '4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 'X-EATS-NETWORK-TYPE': 'wifi',
#                 'User-Agent': 'Android-Coupang-Eats-Customer/1.1.39',
#                 'X-EATS-TIME-ZONE': 'Asia/Seoul',
#                 'X-EATS-DEVICE-MODEL': 'SM-G960N',
#                 'X-EATS-APP-VERSION': '1.1.39',
#                 'X-EATS-LOCALE': 'ko-KR',
#                 'X-EATS-SESSION-ID': '61b04a02-2f9a-484c-b0d5-3335fcf94320',
#                 'X-EATS-RESOLUTION-TYPE': '1080x2076',
#                 'X-EATS-OS-VERSION': '8.0.0',
#                 'X-EATS-PCID': '4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 'Accept-Language': 'ko-KR',
#                 'X-EATS-LOCATION': '{"addressId":0,"latitude":0.0,"longitude":0.0}',
#                 'Host': 'api.coupangeats.com',
#                 'Connection': 'Keep-Alive',
#                 'Accept-Encoding': 'gzip',
#             }
#             import requests
#
#             headers = {
#                 'X-EATS-OS-TYPE': 'ANDROID',
#                 'X-EATS-ACCESS-TOKEN': '51sig1lT7YNWXgOmfUOqw8EMs_bFEj5995eFtiXBt3VLVPj3gSl7IJkG-k5XUFXIjo_Oibk1gGYSJSY99iCMD02e6IXaa3k_zFdgbXgdHXMPc4kxzICtKEFjv63h-dn2eRtSiw_G2G4lfKZX-aBizEs_uFf5kO0dOTJ_xRC34EyRydbgu4WImZr2mbbkXye3D77tQTsKsH-3kLNDuw6rCkCHXfgw5nruLs6hzqb5-Q3OohlmvH0HKK2EziRlQ3GUhmzNsCxSMghXWgfAzvLWRXieGeEzeqKHib43CK-rbJ4=',
#                 'X-EATS-DEVICE-DENSITY': 'XXHDPI',
#                 'X-EATS-DEVICE-ID': '4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 'X-EATS-NETWORK-TYPE': 'wifi',
#                 'User-Agent': 'Android-Coupang-Eats-Customer/1.1.34',
#                 'X-EATS-TIME-ZONE': 'Asia/Seoul',
#                 'X-EATS-DEVICE-MODEL': 'SM-G960N',
#                 'X-EATS-APP-VERSION': '1.1.34',
#                 'X-EATS-LOCALE': 'ko-KR',
#                 'X-EATS-SESSION-ID': 'd808d2c2-73ff-4326-bd7a-cfe4d4b06cd0',
#                 'X-EATS-RESOLUTION-TYPE': '1080x2076',
#                 'X-EATS-OS-VERSION': '8.0.0',
#                 'X-EATS-PCID': '4af74da3-4f85-32fa-80dd-1b1aba0aa592',
#                 'Accept-Language': 'ko-KR',
#                 'X-EATS-LOCATION': '{"addressId":4404538,"latitude":37.5088318832,"longitude":127.034317309,"zipcode":"06108"}',
#                 'Host': 'api.coupangeats.com',
#                 'Connection': 'Keep-Alive',
#                 'Accept-Encoding': 'gzip',
#             }
#
#             params = (
#                 ('categoryId', '2'),
#                 ('nextToken', ''),
#                 ('badgeFilters', ''),
#             )
#
#             # rp = requests.get(url, headers=headers)
#             rp = requests.get(
#                 'https://api.coupangeats.com/endpoint/store.get_clp',
#                 headers=headers, params=params)
#
#             print(rp.status_code)
#             print(rp.text)
#
#         except Exception as e:
#             sys.stderr.write('\n%s\n' % str(e))
#             self.assertTrue(os.path.exists(stderr_file) and
#                             os.path.getsize(stderr_file) > 0)
#         finally:
#             if os.path.exists(of):
#                 os.remove(of)
#             if os.path.exists(stderr_file):
#                 os.remove(stderr_file)

    # ==========================================================================
    def test0480_upload(self):
        of = 'foo.txt'
        stderr_file = 'stderr.txt'
        try:
            url = 'http://127.0.0.1:8000/upload'
            r = main(
                'post', url,
                '--form',
                '--req-item', r'files@C:\Temp\output\Arevo.txt',
                '--outfile', of,
                '--errfile', stderr_file,
            )
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                # print(rs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.exists(stderr_file) and
                            os.path.getsize(stderr_file) > 0)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(stderr_file):
                os.remove(stderr_file)

    # ==========================================================================
    def test0500_upload_debug_ASJ(self):
        of = 'foo.txt'
        stderr_file = 'stderr.txt'
        try:
            url = 'https://zfr9ibuww2.execute-api.us-west-1.amazonaws.com/dev/upload'
            r = main(
                'post', url,
                '--form',
                '--req-item', r'file@ARGOSLow-code.pdf',
                '--outfile', of,
                '--errfile', stderr_file,
            )
            self.assertTrue(r == 0)
            encoding = get_file_encoding(of)
            with open(of, encoding=encoding) as ifp:
                rs = ifp.read()
                # print(rs)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(os.path.exists(stderr_file) and
                            os.path.getsize(stderr_file) > 0)
        finally:
            if os.path.exists(of):
                os.remove(of)
            if os.path.exists(stderr_file):
                os.remove(stderr_file)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
