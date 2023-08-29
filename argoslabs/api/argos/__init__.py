#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.api.argos`
====================================
.. moduleauthor:: Kyobong An <akb0930@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS OPEN API
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2022/04/07]
#     - apiurl 기능추가.
#  * [2021/11/29]
#     - sendOndemand에 최소 입력값을 userid,scnarioid,pamid로만 줄임. 기존에 봇파라미터값이 있어야 작동했슴.
#  * [2021/09/02]
#     - 출력되는 부분 수정 csv타입으로 변경
#  * [2021/08/30]
#     - starting

################################################################################
import os
import yaml
import sys
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


def safe_eval(value, default=None):
    try:
        if not value:
            return default
        r = eval(value)
        return r
    except Exception:
        # return default, string type return
        return value if value else default


################################################################################
# noinspection PyBroadException
class OpenApi(object):
    def __init__(self, argspec):
        self.argspec = argspec
        # %homepath%에 .argos-rpa-config.yaml 파일이 있어도 내용이 다를 수 있음.
        rpa_config_f = os.path.expanduser(os.path.join('~', '.argos-rpa-config.yaml'))
        try:
            with open(rpa_config_f) as ifp:
                argos_config = yaml.load(ifp, yaml.SafeLoader)
                self.api_url = argos_config[-1]['ApiHost']
        except Exception as e:
            self.api_url = 'https://api2-rpa.argos-labs.com'
        if self.argspec.apiurl:
            self.api_url = argspec.apiurl

        self.api = argspec.api
        self.apikey = argspec.apikey

        if self.api == "getPamList":
            self.getpamList()
        elif self.api == "getBotList":
            self.getbotlist()
        else:
            self.botparameters = []
            if argspec.valuename:
                self.get_botparameters()
            self.sendondemand()

    # ==========================================================================
    def getpamList(self):
        self.api_url += "///openapi/v1/pam/list?apiKey="
        xml = requests.get(self.api_url+self.apikey)
        if xml.json()['status']//10 == 20:  # 정상일경우는 20x 기때문에 나머지는 에러처리.
            for i in xml.json()['data']:
                for k, v in i.items():
                    sys.stdout.write("%s,%s,\n" % (k, v))
                    # self.output.append("%s,%s" % (k, v))
            # sys.stdout.write(",".join(self.output))
        else:
            sys.stderr.write("status : %d" % xml.json()['status'])
            raise Exception()
        # sys.stdout.write(xml.json()['data'])

    # ==========================================================================
    def getbotlist(self):
        self.api_url += "///openapi/v1/scenario/list?apiKey="
        xml = requests.get(self.api_url+self.apikey)
        if xml.json()['status']//10 == 20:  # 정상일경우는 20x 기때문에 나머지는 에러처리.
            for i in xml.json()['data']:
                for k, v in i.items():
                    sys.stdout.write("%s,%s,\n" % (k, v))
        else:
            sys.stderr.write("status : %d" % xml.json()['status'])
            raise Exception()
        # sys.stdout.write(xml.text)

    # ==========================================================================
    def sendondemand(self):
        self.api_url += "///openapi/v1/uxrobot/remote_command/ondemandrun/api?apiKey="
        xml = requests.post(self.api_url+self.apikey, json={"userId": self.argspec.userid,
                                                            "apiScenarioId": self.argspec.scenarioid,
                                                            "apiPamId": self.argspec.pamid,
                                                            "endPoint": self.argspec.endpoint,
                                                            "workId": self.argspec.workid,
                                                            "botParameters": self.botparameters})
        if xml.json()['status']//10 == 20:  # 정상일경우는 20x 기때문에 나머지는 에러처리.
            for i in xml.json()['data']:
                for k, v in i.items():
                    if k == "commandResponse":  # commdanRespomse 값만 형식 변환.
                        sys.stdout.write("%s,%s,\n" % (k, str(v)))
                    else:
                        sys.stdout.write("%s,%s,\n" % (k, v))
        else:
            sys.stderr.write("status : %d" % xml.json()['status'])
            raise Exception()
        # sys.stdout.write(xml.text)

    # ==========================================================================
    def get_botparameters(self):
        for i, valuename in enumerate(self.argspec.valuename):  # variable_text에{{}}를 내부적으로 입력해주어야함.
            a = {"variable_text": "{{"+valuename+"}}", "value": safe_eval(self.argspec.value[i])}
            self.botparameters.append(a)


################################################################################
@func_log
def func(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        OpenApi(argspec)
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
    with ModuleContext(
            owner='ARGOS-LABS',
            group='9',
            version='1.1.1',
            platform=['windows', 'darwin', 'linux'],
            output_type='csv',
            display_name='Supervisor API',
            icon_path=get_icon_path(__file__),
            description='Supervisor OPEN API',
    ) as mcxt:
        # #####################################  for app dependent parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('api',
                          display_name='API',
                          choices=['getPamList', 'getBotList', 'sendOndemand'],
                          help='Select the api')
        # ----------------------------------------------------------------------
        mcxt.add_argument('apikey',
                          display_name='API Key',
                          input_method='password',
                          help='Enter your apikey')
        # ######################################  for app optional parameters
        # ----------------------------------------------------------------------
        mcxt.add_argument('--userid', display_name='User ID',
                          input_group='sendOndemand',
                          help='User ID.')
        mcxt.add_argument('--scenarioid', display_name='Scenario ID',
                          input_group='sendOndemand',
                          help='One of Scenario id from a scenario list.')
        mcxt.add_argument('--pamid', display_name='Pam ID',
                          input_group='sendOndemand',
                          help='One of pam id from a pam list.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--endpoint', display_name='End Point',
                          input_group='sendOndemand',
                          help="API User's Webhook URL Value.")
        mcxt.add_argument('--workid', display_name='Work ID',
                          input_group='sendOndemand',
                          help='Other Job/Work id for API User.')
        mcxt.add_argument('--valuename',
                          display_name='Variable_Text', action='append',
                          input_group='sendOndemand',
                          help='The parameter name to use for the pam operation. (eg, "my.a")')
        mcxt.add_argument('--value', display_name='Value', action='append',
                          input_group='sendOndemand',
                          help='The parameter value to use for the pam operation.')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--apiurl', display_name='API URL',
                          help='Enter thr API URL')

        argspec = mcxt.parse_args(args)
        return func(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
