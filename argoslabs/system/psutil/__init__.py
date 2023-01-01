"""
====================================
 :mod:`argoslabs.system.psutil`
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
#  * [2021/03/31]
#     - 그룹에 "1002-Verifications" 넣음
#  * [2021/03/03]
#     - class PSUtil
#  * [2021/03/02]
#     - starting

################################################################################
import os
import sys
import csv
import psutil
import datetime
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class PSUtil(object):
    # ==========================================================================
    OP_LIST = [
        'Get Process',
        'CPU Percent',
        'CPU Count',
        'Load Avg',
        'Memory Info',
        'Disk Info',
        'Network Stats',
        'Network Conns',
        'NIC Address',
        'NIC Info',
    ]
    PROCESS_HEADER = [
        'pid', 'ppid', 'status', 'name', 'exe', 'memory_percent',
        'cpu_percent', 'cwd', 'create_time', 'username',  # 'cmdline'
    ]

    # ==========================================================================
    def __init__(self, logger):
        self.logger = logger
        self.cw = csv.writer(sys.stdout, lineterminator='\n')

    # ==========================================================================
    def cpu_percent(self):
        header = list()
        row = list()
        cps = psutil.cpu_percent(interval=None, percpu=True)
        cp_all = psutil.cpu_percent(interval=None, percpu=False)
        if isinstance(cps, (list, tuple)):
            row.extend(cps)
        else:
            row.append(cps)
        for i in range(len(row)):
            header.append(f'cpu{i+1}_percent')
        header.append('cpu_percent')
        row.append(cp_all)
        self.cw.writerow(header)
        self.cw.writerow(row)

    # ==========================================================================
    def cpu_count(self, logical=False):
        header = list()
        row = psutil.cpu_count(logical=logical)
        header.append(f'cpu_count')
        self.cw.writerow(header)
        self.cw.writerow([row])

    # ==========================================================================
    def getloadavg(self):
        header = ('last_1m_load', 'last_5m_load', 'last_15m_load')
        row = psutil.getloadavg()
        self.cw.writerow(header)
        self.cw.writerow(row)

    # ==========================================================================
    def virtual_memory(self):
        header = ('total', 'available', 'percent', 'used', 'free')
        r = psutil.virtual_memory()
        self.cw.writerow(header)
        self.cw.writerow([
            r.total,
            r.available,
            r.percent,
            r.used,
            r.free,
        ])

    # ==========================================================================
    def disk_info(self):
        header = ('device', 'mountpoint', 'fstype', 'opts', 'maxfile', 'maxpath',
                  'total', 'used', 'free', 'percent')
        rds = psutil.disk_partitions()
        self.cw.writerow(header)
        for rd in rds:
            row = [
                rd.device,
                rd.mountpoint,
                rd.fstype,
                rd.opts,
                rd.maxfile,
                rd.maxpath,
            ]
            try:
                du = psutil.disk_usage(rd.mountpoint)
                row.extend([
                    du.total,
                    du.used,
                    du.free,
                    du.percent,
                ])
            except:
                row.extend(['', '', '', ''])
            self.cw.writerow(row)

    # ==========================================================================
    def net_info(self):
        header = ('nic', 'bytes_sent', 'bytes_recv', 'packets_sent', 'packets_recv',
                  'errin', 'errout', 'dropin', 'dropout')
        self.cw.writerow(header)
        nios = psutil.net_io_counters(pernic=True)
        for nic, nio in nios.items():
            row = [
                nic,
                nio.bytes_sent,
                nio.bytes_recv,
                nio.packets_sent,
                nio.packets_recv,
                nio.errin,
                nio.errout,
                nio.dropin,
                nio.dropout,
            ]
            self.cw.writerow(row)

    # ==========================================================================
    def net_connections(self):
        header = ('family', 'type', 'local_addr_ip', 'local_addr_port',
                  'remote_addr_ip', 'remote_addr_port', 'status', 'pid')
        self.cw.writerow(header)
        ncs = psutil.net_connections()
        for nc in ncs:
            row = [
                str(nc.family).split('.')[-1],
                str(nc.type).split('.')[-1],
                nc.laddr.ip if nc.laddr else '',
                nc.laddr.port if nc.laddr else '',
                nc.raddr.ip if nc.raddr else '',
                nc.raddr.port if nc.raddr else '',
                nc.status,
                nc.pid,
            ]
            self.cw.writerow(row)

    # ==========================================================================
    def net_if_addrs(self):
        header = ('nic', 'family', 'address', 'netmask', 'broadcast', 'ptp')
        self.cw.writerow(header)
        nia = psutil.net_if_addrs()
        for nic, nis in nia.items():
            for ni in nis:
                row = [
                    nic,
                    str(ni.family).split('.')[-1],
                    ni.address,
                    ni.netmask if ni.netmask else '',
                    ni.broadcast if ni.broadcast else '',
                    ni.ptp if ni.ptp else '',
                ]
                self.cw.writerow(row)

    # ==========================================================================
    def net_if_stats(self):
        header = ('nic', 'isup', 'duplex', 'speed', 'mtu')
        self.cw.writerow(header)
        nis = psutil.net_if_stats()
        for nic, ni in nis.items():
            row = [
                nic,
                ni.isup,
                str(ni.duplex).split('.')[-1],
                ni.speed,
                ni.mtu,
            ]
            self.cw.writerow(row)

    # ==========================================================================
    def get_boot_time(self):
        header = ('boottime',)
        self.cw.writerow(header)
        bt = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        self.cw.writerow([bt])

    # ==========================================================================
    def get_processes(self, procname=None):
        pids = list()
        for p in psutil.process_iter(['name', 'pid']):
            rd = p.as_dict(self.PROCESS_HEADER)
            if procname:
                if not rd['name']:
                    continue
                if rd['name'].lower().find(procname.lower()) < 0:
                    continue
            pids.append(rd['pid'])
        if not pids:
            return len(pids)
        self.cw.writerow(self.PROCESS_HEADER)
        d_pids = list()
        for pid in pids:
            try:
                p = psutil.Process(pid)
            except:
                d_pids.append(pid)
                continue
            rd = p.as_dict(self.PROCESS_HEADER)
            row = list()
            for h in self.PROCESS_HEADER:
                if h in rd:
                    v = rd[h]
                    if h == 'create_time':
                        if v > 0.0:
                            v = datetime.datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")
                    elif h == 'cmdline':
                        v = ','.join(v)
                    row.append(v)
                else:
                    row.append('')
            self.cw.writerow(row)
        for d_pid in d_pids:
            pids.remove(d_pid)
        return len(pids)


################################################################################
@func_log
def do_psutil(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        pu = PSUtil(logger=mcxt.logger)
        if argspec.op == PSUtil.OP_LIST[0]:     # 'Get Process'
            r = pu.get_processes(procname=argspec.pname)
            if r <= 0:
                return 1    # No matching processes
        elif argspec.op == PSUtil.OP_LIST[1]:   # 'CPU Percent'
            pu.cpu_percent()
        elif argspec.op == PSUtil.OP_LIST[2]:   # 'CPU Count'
            pu.cpu_count()
        elif argspec.op == PSUtil.OP_LIST[3]:   # 'Load Avg'
            pu.getloadavg()
        elif argspec.op == PSUtil.OP_LIST[4]:   # 'Memory Info'
            pu.virtual_memory()
        elif argspec.op == PSUtil.OP_LIST[5]:   # 'Disk Info'
            pu.disk_info()
        elif argspec.op == PSUtil.OP_LIST[6]:   # 'Network Stats'
            pu.net_info()
        elif argspec.op == PSUtil.OP_LIST[7]:   # 'Network Conns'
            pu.net_connections()
        elif argspec.op == PSUtil.OP_LIST[8]:   # 'NIC Address'
            pu.net_if_addrs()
        elif argspec.op == PSUtil.OP_LIST[9]:   # 'NIC Info'
            pu.net_if_stats()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 99
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
        group='1002',   # Verifications
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Sys Info',
        icon_path=get_icon_path(__file__),
        description='Get System Info (Process, CPU, Mem, HDD, Network)',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          choices=PSUtil.OP_LIST,
                          display_name='Operation',
                          help='Which operation for System information')
        # ######################################## for app dependent options
        mcxt.add_argument('--pname',
                          display_name='Proc Name',
                          show_default=True,
                          help='Process name for partial search')
        argspec = mcxt.parse_args(args)
        return do_psutil(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
