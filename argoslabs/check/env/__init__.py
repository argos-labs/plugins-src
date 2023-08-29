#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.check.env`
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
#  * [2023/03/06]kyobong
#     - csv 타입 일때 key(width_mm, height_mm, scale)값이 없어 에러발생
#  * [2021/03/26]
#     - 그룹에 "9-Utility Tools" 넣음
#  * [2020/07/08]
#     - starting

################################################################################
import os
import sys
import csv
import json
import yaml
import winreg
import psutil
import locale
import ctypes
import platform
import requests
import pyautogui
from pathlib import Path
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvnet import is_svc_opeded
# from argoslabs.check.env.screeninfo import get_monitors
from screeninfo import get_monitors
from speedtest import Speedtest


################################################################################
class EnvCheck(object):
    # ==========================================================================
    OUTPUT_FORMAT = ('csv', 'json', 'yaml')
    SERVICES = [
        ('supervisor', 'rpa.argos-labs.com', 443),
        ('pypi', 'pypi.org', 443),
        ('pypi_files', 'files.pythonhosted.org', 443),
    ]

    # ==========================================================================
    def __init__(self, output_format, is_network_speed_check=False):
        if output_format not in self.OUTPUT_FORMAT:
            raise RuntimeError(f'Invalid output format "{output_format}"')
        self.output_format = output_format
        self.is_network_speed_check = is_network_speed_check
        self.result = {}

    # ==========================================================================
    @staticmethod
    def _hr_bytes(v):
        if v > 1024*1024*1024*1024:
            v /= 1024*1024*1024*1024
            return f'{round(v,2)}T'
        if v > 1024*1024*1024:
            v /= 1024*1024*1024
            return f'{round(v,2)}G'
        if v > 1024*1024:
            v /= 1024*1024
            return f'{round(v,2)}M'
        if v > 1024:
            v /= 1024
            return f'{round(v,2)}K'
        return f'{v}B'

    # ==========================================================================
    def get_platform(self):
        self.result['platform'] = {
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }

    # ==========================================================================
    def get_public_ip_address(self):
        self.result['public_ip'] = 'Not available'
        # noinspection PyBroadException
        try:
            rp = requests.get('https://api.ipify.org')
            if rp.status_code // 10 == 20:
                self.result['public_ip'] = rp.text
                # print('Public IP address is:', rp.text)
        except Exception:
            pass

    # ==========================================================================
    def get_cpu(self):
        self.result['cpu'] = {
            'count': psutil.cpu_count(),
            'percent': f'{psutil.cpu_percent(interval=None)}%',
        }

    # ==========================================================================
    def get_memory(self):
        vm = psutil.virtual_memory()
        self.result['memory'] = {
            'total': self._hr_bytes(vm.total),
            'percent': f'{vm.percent}%',
        }

    # ==========================================================================
    def get_disk(self):
        self.result['disks'] = []
        for i, dp in enumerate(psutil.disk_partitions()):
            # noinspection PyBroadException
            try:
                dpu = psutil.disk_usage(dp.mountpoint)
                dpd = {
                    'device': dp.device,
                    'total': self._hr_bytes(dpu.total),
                    'percent': f'{dpu.percent}%',
                }
                self.result['disks'].append(dpd)
            except Exception:
                pass

    # ==========================================================================
    def check_screen(self):
        self.result['monitors'] = []
        try:
            for i, m in enumerate(get_monitors()):
                md = {
                    'name': m.name,
                    'width': m.width,
                    'height': m.height,
                    'width_mm': m.width_mm,
                    'height_mm': m.height_mm,
                    'scale': m.scale,
                }
                self.result['monitors'].append(md)
        except:
            s = pyautogui.size()
            md = {
                'name': 'monitor',
                'width': s.width,
                'height': s.height,
            }
            self.result['monitors'].append(md)

    # ==========================================================================
    def check_services(self):
        self.result['services'] = []
        for name, host, port in self.SERVICES:
            svcd = {
                'name': name,
                'host': host,
                'port': port,
                'opened': 'opened' if is_svc_opeded(host, port) else 'closed',
            }
            self.result['services'].append(svcd)

    # ==========================================================================
    def get_network_speed(self):
        st = Speedtest()
        self.result['network'] = {
            'download_speed': f'{self._hr_bytes(st.download())}Bit/s',
            'upload_speed': f'{self._hr_bytes(st.upload())}Bit/s',
        }

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_preffered_langs(self):
        pls = []
        key = None
        # noinspection PyBroadException
        try:
            proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
            proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()

            if proc_arch == 'x86' and not proc_arch64:
                arch_key = 0
            elif proc_arch == 'x86' or proc_arch == 'amd64':
                arch_key = winreg.KEY_WOW64_64KEY
            else:
                raise Exception("Unhandled arch: %s" % proc_arch)

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\CTF\SortOrder\Language", 0,
                                 winreg.KEY_READ | arch_key)
            # 현재는 10개 까지만
            for i in range(10):
                pl = winreg.QueryValueEx(key, '0000000%d' % i)
                pls.append(int(pl[0].lstrip('0'), 16))
        except Exception:
            pass
        finally:
            if key is not None:
                key.Close()
            return pls

    # ==========================================================================
    def get_lang(self):
        windll = ctypes.windll.kernel32
        slang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
        plangs = self._get_preffered_langs()
        self.result['language'] = {
            'default': slang,
            'preffered': [],
        }
        for plang in plangs:
            self.result['language']['preffered'].append(locale.windows_locale[plang])

    # ==========================================================================
    def get_env_var(self):
        self.result['env_vars'] = evs = {}
        for k, v in os.environ.items():
            evs[k] = v

    # ==========================================================================
    def output_csv(self):
        header = [
            'platform', 'machine', 'processor', 'public_ip',
            'cpu_count', 'cpu_percent',
            'mem_total', 'mem_percent',
        ]
        for i, dpd in enumerate(self.result['disks']):
            header.append(f'disk{i+1}_device')
            header.append(f'disk{i+1}_total')
            header.append(f'disk{i+1}_percent')
        for i, md in enumerate(self.result['monitors']):
            header.append(f'monitors{i+1}_name')
            header.append(f'monitors{i+1}_width')
            header.append(f'monitors{i+1}_height')
            # header.append(f'monitors{i+1}_width_mm')
            # header.append(f'monitors{i+1}_height_mm')
            # header.append(f'monitors{i + 1}_scale')
        for i, svcd in enumerate(self.result['services']):
            header.append(f'svc_{svcd["name"]}')
        header.append('language')
        for i, pl in enumerate(self.result['language']['preffered']):
            header.append(f'lang_{i+1}')
        if self.is_network_speed_check:
            header.append('download_speed')
            header.append('upload_speed')
        row = [
            self.result['platform']['platform'],
            self.result['platform']['machine'],
            self.result['platform']['processor'],
            self.result['public_ip'],
            self.result['cpu']['count'],
            self.result['cpu']['percent'],
            self.result['memory']['total'],
            self.result['memory']['percent'],
            # f"{self.result['supervisor']['host']}:{self.result['supervisor']['port']} {self.result['supervisor']['opened']}",
        ]
        for dpd in self.result['disks']:
            row.append(dpd['device'])
            row.append(dpd['total'])
            row.append(dpd['percent'])
        for md in self.result['monitors']:
            row.append(md['name'])
            row.append(md['width'])
            row.append(md['height'])
            # row.append(md['width_mm'])
            # row.append(md['height_mm'])
            # row.append(md['scale'])
        for svcd in self.result['services']:
            row.append(f'{svcd["opened"]}')
        row.append(self.result['language']['default'])
        for i, pl in enumerate(self.result['language']['preffered']):
            row.append(pl)
        if self.is_network_speed_check:
            row.append(self.result['network']['download_speed'])
            row.append(self.result['network']['upload_speed'])
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        c.writerow(row)

    # ==========================================================================
    def output_json(self):
        json.dump(self.result, sys.stdout)

    # ==========================================================================
    def output_yaml(self):
        yaml.dump(self.result, sys.stdout)

    # ==========================================================================
    def get_all(self):
        self.get_platform()
        self.check_screen()
        self.get_cpu()
        self.get_memory()
        self.get_disk()
        self.get_public_ip_address()
        self.check_services()
        self.get_lang()
        self.get_env_var()
        if self.is_network_speed_check:
            self.get_network_speed()
        # 항상 {home}\
        if True:
            stdir = os.path.join(str(Path.home()), '.argos-rpa.test')
            if not os.path.isdir(stdir):
                os.makedirs(stdir)
            ofile = os.path.join(stdir, '.check_env.yaml')
            with open(ofile, 'w') as ofp:
                yaml.dump(self.result, ofp)
        if self.output_format == 'csv':
            return self.output_csv()
        elif self.output_format == 'json':
            return self.output_json()
        elif self.output_format == 'yaml':
            return self.output_yaml()


################################################################################
@func_log
def get_env_all(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        # ec = EnvCheck(argspec.out_format, is_network_speed_check=argspec.is_check_network_speed)
        ec = EnvCheck(argspec.out_format)
        ec.get_all()
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Env Check',
        icon_path=get_icon_path(__file__),
        description='Check if PAM/plugin running environment is OK',
    ) as mcxt:
        # ##################################### for app dependent parameters
        # mcxt.add_argument('host',
        #                   display_name='Host',
        #                   help='Host name of IP address to check')
        # ######################################## for app dependent options
        mcxt.add_argument('--out-format', choices=EnvCheck.OUTPUT_FORMAT,
                          display_name='Output Format', default='csv',
                          show_default=True,
                          help='output format, one of "csv", "json" or "yaml"')
        # mcxt.add_argument('--is-check-network-speed', action='store_true',
        #                   display_name='Chk Net Speed',
        #                   help='If this flag is set then checking network speed which can takes long time, a minute or so.')
        argspec = mcxt.parse_args(args)
        return get_env_all(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
