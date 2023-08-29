#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.argos_service_jp.parsehub_api`
====================================
.. moduleauthor:: Taiki Shimasaki <shimasaki@argos-service.com>
.. note:: ARGOS-LABS License

Description
===========
Input Plugin Description
"""
# Authors
# ===========
#
# * Taiki Shimasaki
#
# Change Log
# --------
#
#  * [20--/--/--]
#     Create

################################################################################
import os
import sys
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import requests
import json
import time

################################################################################
class parsehub_API(object):

    # ==========================================================================
    def __init__(self, operation, api_key, token, ez_mode):
        self.operation = operation
        self.api_key = api_key
        self.token = token
        self.ez_mode = ez_mode

        self.run_token = None
        self.start_value = None
        self.start_url = None
        self.email = None
        self.format = None

        self.params = {
            "api_key": "{}".format(self.api_key)
        }
        self.params_add = None
        self.list_opt = None

        self.status_resp = None
        self.status = None
        self.rt_data = None
        self.rt_json = None
        self.rt_data_list = None

    # ==========================================================================
    def set_run_token(self, run_token):
        if self.operation == 'Get Projects List':
            raise KeyError('Uncheck \"Run Token\" field!')

        elif self.operation == 'Run Project':
            raise KeyError('Uncheck \"Run Token\" field!')

        elif self.operation == 'Get Data':
            if run_token:
                self.run_token = run_token
            elif run_token == '':
                raise IOError('Input \"Run Token\" field!')

        elif self.operation == 'Get Last Run':
            if run_token:
                self.run_token = run_token
            elif run_token == '':
                raise KeyError('Uncheck \"Run Token\" field!')

        elif self.operation == 'Delete Run Data':
            if run_token:
                self.run_token = run_token
            elif run_token == '':
                raise IOError('Input \"Run Token\" field!')

    # ==========================================================================
    def set_start_url(self, start_url):
        if self.operation == 'Get Projects List':
            raise KeyError('Uncheck \"Start URL\" field!')

        elif self.operation == 'Run Project':
            if start_url:
                self.start_url = start_url
                self.params["start_url"] = "{}".format(self.start_url)
            elif start_url == '':
                raise IOError('Input \"Start URL\" field!')

        elif self.operation == 'Get Data':
            raise KeyError('Uncheck \"Start URL\" field!')

        elif self.operation == 'Get Last Run':
            raise KeyError('Uncheck \"Start URL\" field!')

        elif self.operation == 'Delete Run Data':
            raise KeyError('Uncheck \"Start URL\" field!')

    # ==========================================================================
    def set_start_val(self, start_value):
        if self.operation == 'Get Projects List':
            raise KeyError('Uncheck \"Start Value\" field!')

        elif self.operation == 'Run Project':
            if start_value:
                self.start_value = start_value
                self.params["start_value_override"] = "{}".format(self.start_value)
            elif start_value == '':
                raise IOError('Input \"Start Value\" field!')

        elif self.operation == 'Get Data':
            raise KeyError('Uncheck \"Start Value\" field!')

        elif self.operation == 'Get Last Run':
            raise KeyError('Uncheck \"Start Value\" field!')

        elif self.operation == 'Delete Run Data':
            raise KeyError('Uncheck \"Start Value\" field!')

    # ==========================================================================
    def set_email(self, email):
        if email == 'ON':
            self.email = '1'
        elif email == 'OFF':
            self.email = '0'

        if self.operation == 'Get Projects List':
            pass

        elif self.operation == 'Run Project':
            self.params["send_email"] = "{}".format(self.email)

        elif self.operation == 'Get Data':
            pass

        elif self.operation == 'Get Last Run':
            pass

        elif self.operation == 'Delete Run Data':
            pass

    # ==========================================================================
    def set_format(self, format):
        self.format = format

        if self.operation == 'Get Projects List':
            pass

        elif self.operation == 'Run Project':
            pass

        elif self.operation == 'Get Data':
            self.params["format"] = "{}".format(self.format)

        elif self.operation == 'Get Last Run':
            pass

        elif self.operation == 'Delete Run Data':
            pass

    # ==========================================================================
    def set_params(self):
        if self.operation == 'Get Projects List':
            if self.ez_mode == 'OFF':
                self.list_opt = '1'
            elif self.ez_mode == 'ON':
                self.list_opt = '0'
            self.params_add = {
                "offset": "0",
                "limit": "20",
                "include_options": "{}".format(self.list_opt)
            }
            self.params.update(self.params_add)

        elif self.operation == 'Run Project':
            self.params_add = {
                "start_template": "main_template",
            }
            self.params.update(self.params_add)

        elif self.operation == 'Get Data':
            self.params_add = {}

        elif self.operation == 'Get Last Run':
            self.params_add = {
                "offset": "0"
            }
            self.params.update(self.params_add)

        elif self.operation == 'Delete Run Data':
            self.params_add = {}

        else:
            pass

    # ==========================================================================
    def select_operations(self):
        if self.operation == '':
            raise IOError('Choose Any Operations!')

        elif self.operation == 'Get Projects List':
            return 'get list'

        elif self.operation == 'Run Project':
            return 'run'

        elif self.operation == 'Get Data':
            return 'get'

        elif self.operation == 'Get Last Run':
            return 'last'

        elif self.operation == 'Delete Run Data':
            return 'del'

        else:
            raise IOError('Unexpected Error Occurred')

    # ==========================================================================
    def get_list(self):
        self.rt_data = requests.get("https://www.parsehub.com/api/v2/projects",
                                    params=self.params)

        if self.ez_mode == 'OFF':
            self.rt_data = self.rt_data.text.replace('\\', '')
        elif self.ez_mode == 'ON':
            self.rt_data = self.rt_data.json()
            self.rt_data_list = self.rt_data["projects"]
            for i in self.rt_data_list:
                i.pop("templates_json")
                i.pop("last_ready_run")
                i.pop("last_run")

            self.rt_data["projects"] = self.rt_data_list

        print(self.rt_data)

    # ==========================================================================
    def run_project(self):
        self.rt_data = requests.post("https://www.parsehub.com/api/v2/projects/{}/run".format(self.token),
                                     data=self.params)

        if self.ez_mode == 'OFF':
            print(self.rt_data.text)
        elif self.ez_mode == 'ON':
            self.rt_json = json.loads(self.rt_data.text)
            self.rt_data = self.rt_json["run_token"]
            print(self.rt_data, end='')

    # ==========================================================================
    def get_data(self):
        self.status_resp = requests.get("https://www.parsehub.com/api/v2/runs/{}".format(self.run_token),
                                        params=self.params)
        self.status = json.loads(self.status_resp.text)["status"]

        if self.status == "complete":
            pass
        elif self.status == "cancelled":
            raise IOError('That run has been canceled.')
        elif self.status == "error":
            raise IOError('An unexpected run error has occurred.')
        else:
            pass

        while self.status == "running":
            time.sleep(0.25)
            self.status_resp = requests.get(
                "https://www.parsehub.com/api/v2/runs/{}".format(
                    self.run_token),
                params=self.params)
            self.status = json.loads(self.status_resp.text)["status"]

            if self.status == "complete":
                break
            elif self.status == "cancelled":
                raise IOError('That run has been canceled.')
            elif self.status == "error":
                raise IOError('An unexpected run error has occurred.')
            else:
                pass

        self.rt_data = requests.get("https://www.parsehub.com/api/v2/runs/{}/data".format(self.run_token),
                                    params=self.params)

        if self.ez_mode == 'OFF':
            print(self.rt_data.text)
        elif self.ez_mode == 'ON':
            if self.format == 'json':
                self.rt_json = json.loads(self.rt_data.text)
                for val in self.rt_json.values():
                    print(val)
            elif self.format == 'csv':
                print(self.rt_data.text)

        """
        if self.ez_mode == 'OFF':
            print(self.rt_data.text)
        elif self.ez_mode == 'ON':
            self.rt_json = json.loads(self.rt_data.text)
            print(self.rt_json[])
        """

    # ==========================================================================
    def get_last(self):
        self.rt_data = requests.get('https://www.parsehub.com/api/v2/projects/{}'.format(self.token),
                                    params=self.params)

        if self.ez_mode == 'OFF':
            self.rt_json = json.loads(self.rt_data.text)
            self.rt_data = self.rt_json["last_run"]
            print(self.rt_data)
        elif self.ez_mode == 'ON':
            self.rt_json = json.loads(self.rt_data.text)
            self.rt_data_list = self.rt_json["last_run"]
            """
            self.rt_data_list.pop("options_json")
            self.rt_data_list.pop("template_pages")
            self.rt_data_list.pop("start_template")
            """
            d = self.rt_data_list
            del d["options_json"], d["template_pages"], d["start_template"]
            del d["custom_proxies"], d["is_empty"], d["md5sum"]
            self.rt_data = d
            print(self.rt_data)

    # ==========================================================================
    def del_data(self):
        self.rt_data = requests.delete("https://www.parsehub.com/api/v2/runs/{}".format(self.run_token),
                                       params=self.params)

        if self.ez_mode == 'OFF':
            print(self.rt_data.text)
        elif self.ez_mode == 'ON':
            self.rt_json = json.loads(self.rt_data.text)
            self.rt_data = self.rt_json["run_token"]
            print(self.rt_data, end='')

################################################################################
@func_log
def parsehub_api(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        ph = parsehub_API(argspec.operation, argspec.api_key, argspec.token, argspec.ez_mode)

        if argspec.run_token:
            ph.set_run_token(argspec.run_token)
        if argspec.start_url:
            ph.set_start_url(argspec.start_url)
        if argspec.start_value:
            ph.set_start_val(argspec.start_value)
        if argspec.email:
            ph.set_email(argspec.email)
        if argspec.format:
            ph.set_format(argspec.format)

        ph.set_params()

        if ph.select_operations() == 'get list':
            ph.get_list()

        elif ph.select_operations() == 'run':
            ph.run_project()

        elif ph.select_operations() == 'get':
            ph.get_data()

        elif ph.select_operations() == 'last':
            ph.get_last()

        elif ph.select_operations() == 'del':
            ph.del_data()

        mcxt.logger.info('>>>end...')
        return 0

    except KeyError as key_err:
        msg = str(key_err)
        mcxt.logger.error(key_err)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1

    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 2

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
        owner='ARGOS-SERVICE-JAPAN',
        group='10',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='parsehub',
        icon_path=get_icon_path(__file__),
        description='Use parsehub API',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('operation',
                          display_name='Operation',
                          choices=[
                              'Get Projects List',
                              'Run Project',
                              'Get Data',
                              'Get Last Run',
                              'Delete Run Data'
                          ],
                          help='Select the operation you want to perform')
        mcxt.add_argument('api_key',
                          display_name='API Key',
                          input_method='password',
                          help='Input thr API Key')
        mcxt.add_argument('token',
                          display_name='Project Token',
                          input_method='password',
                          help='Input the Project Token')
        mcxt.add_argument('ez_mode',
                          display_name='Simple Mode',
                          choices=['ON', 'OFF'],
                          default='ON',
                          show_default=True,
                          help='Turning \'ON\' this mode will simplify the \'Return Value\',\n'
                               'when \'OFF\', it\'s a normal json return value')
        # ######################################## for app dependent options
        mcxt.add_argument('--run_token',
                          display_name='Run Token',
                          show_default=True,
                          input_method='password',
                          help='Input thr Run Token')
        mcxt.add_argument('--start_url',
                          display_name='Start URL',
                          help='Input when overwriting the Start URL')
        mcxt.add_argument('--start_value',
                          display_name='Start Value',
                          help='Input when overwriting the Start Value')
        mcxt.add_argument('--email',
                          display_name='Send Email',
                          default='ON',
                          choices=['ON', 'OFF'],
                          help='When turned \'ON\', a notification e-mail will be sent\n'
                               'when the project is executed')
        mcxt.add_argument('--format',
                          display_name='Returned Format',
                          default='json',
                          choices=['json', 'csv'],
                          help='Select the format of the return value of the executed data')

        argspec = mcxt.parse_args(args)
        return parsehub_api(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass