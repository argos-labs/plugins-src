"""
====================================
 :mod:`argoslabs.aaa.ldap`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for LDAP / ActiveDirectory
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
#  * [2019/11/22]
#     - starting

################################################################################
import os
import sys
import csv
import ldap
import ldap.modlist as modlist
# import chardet
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
# noinspection PyUnresolvedReferences,PyBroadException
class LdapOp(object):
    # ==========================================================================
    OP = [
        'Get',
        'Search',
        'Modify',
        'Create',
        'Delete'
    ]

    # ==========================================================================
    def __init__(self, args, network_timeout=3):
        self.args = args
        # connection info
        self.host = args.host
        self.port = args.port
        self.user = args.user
        self.passwd = args.passwd
        self.network_timeout = network_timeout
        # for internal
        self.conn = None
        self.r_conn = None
        self.isopend = False

    # ==========================================================================
    def open(self):
        try:
            conn = ldap.initialize('ldap://%s:%s' % (self.host, self.port))
            conn.protocol_version = 3
            conn.network_timeout = self.network_timeout
            conn.set_option(ldap.OPT_REFERRALS, 0)
            _ = conn.simple_bind_s(self.user, self.passwd)
            self.r_conn = "valid crential"
            self.conn = conn
            self.isopend = True
        except ldap.INVALID_CREDENTIALS:
            self.r_conn = "invalid credential"
        except ldap.SERVER_DOWN:
            self.r_conn = 'server down'

    # ==========================================================================
    def close(self):
        sys.stdout.flush()
        sys.stderr.flush()
        if self.conn is not None:
            self.conn.unbind()
            self.conn = None
        self.isopend = False

    # ==========================================================================
    def __enter__(self):
        return self

    # ==========================================================================
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    def _get_user(self):
        return self.user.split('@')[0]

    # ==========================================================================
    def _get_domain(self):
        return self.user.split('@')[1]

    # ==========================================================================
    def _get_base(self):
        if self.user.find('@') < 0:
            raise RuntimeError('User must have the type "user@a.b.c"')
        dcs = list()
        for dc in self.user.split('@')[1].split('.'):
            dcs.append('DC=%s' % dc)
        return ','.join(dcs)

    # ==========================================================================
    def _get_dn(self, user=None):
        if not user:
            user = self._get_user()
        return 'CN=%s,CN=Users,%s' % (user, self._get_base())

    # ==========================================================================
    def _search(self, *args):
        if not (self.isopend and args):
            return []
        base = 'CN=Users,' + self._get_base()
        # base = self._get_base()
        criteria = list()
        for v in args:
            criteria.append('(%s)' % v)
        criteria_str = ''.join(criteria)
        if len(criteria) > 1:
            criteria_str = "(&%s)" % criteria_str
        attributes = ['*']
        result = self.conn.search_s(base, ldap.SCOPE_SUBTREE, criteria_str, attributes)
        results = list()
        for dn, entry in result:
            if not (dn and isinstance(entry, dict)):
                continue
            results.append(entry)
        return results

    # ==========================================================================
    @staticmethod
    def _get_val(v):
        if isinstance(v, bytes):
            try:
                return v.decode('utf-8')
            except Exception:
                # chardet 로도 결과가 이상하여 모두 hex로 출력
                return '0x%s' % v.hex()
                # r = chardet.detect(v)
                # if not r['encoding']:
                #     return '0x%s' % v.hex()
                # return v.decode(r['encoding'])
        return str(v)

    # ==========================================================================
    def search(self):
        if not self.isopend:
            print(self.r_conn, end='')
            return False
        if not (self.args.search_attributes and
                isinstance(self.args.search_attributes, list)):
            raise ValueError('"Attributes to search" must be provided')
        results = self._search(*self.args.search_attributes)
        if not results:
            print("no result", end='')
            return False
        header = list()
        for r in results:
            for k, v in r.items():
                if not (isinstance(v, list) and len(v) == 1):
                    continue
                if k not in header:
                    header.append(k)
        c = csv.writer(sys.stdout, lineterminator='\n')
        c.writerow(header)
        for r in results:
            row = list()
            for h in header:
                if h in r:
                    v = self._get_val(r[h][0])
                else:
                    v = ''
                row.append(v)
            c.writerow(row)
        return True

    # ==========================================================================
    def get(self, user=None):
        if not self.isopend:
            print(self.r_conn, end='')
            return False
        # user 에서 user@a.b.c 앞에 user 만 찾아, name=user 로 검색
        # dn=a,dn=b,dn=c 로
        if not user:
            user = self._get_user()
        self.args.search_attributes = ['name=%s' % user]
        return self.search()

    # ==========================================================================
    @staticmethod
    def _get_attr_format(kv, new_value=None):
        k, v = kv.split('=', maxsplit=1)
        if new_value is None:
            k, v = k.strip(), v.strip()
        else:
            k, v = k.strip(), new_value.strip()
        return {k: [v.encode()]}

    # ==========================================================================
    def modify(self):
        if not self.isopend:
            print(self.r_conn, end='')
            return False
        # if not self.args.modify_from:
        #     raise ValueError('"Old Attr to modify" must be provided')
        if not self.args.modify_to:
            raise ValueError('"New Attr to modify" must be provided')
        user = self.args.modify_user if self.args.modify_user else self._get_user()
        modify_dn = self._get_dn(user)
        # old = self._get_attr_format(self.args.modify_from, new_value='*')
        old = self._get_attr_format(self.args.modify_to, new_value='*')
        new = self._get_attr_format(self.args.modify_to)
        ldif = modlist.modifyModlist(old, new)
        self.conn.modify_s(modify_dn, ldif)
        return self.get(user)

    # ==========================================================================
    def create(self):
        if not self.isopend:
            print(self.r_conn, end='')
            return False
        if not self.args.create_user:
            raise ValueError('"User to create" must be provided')
        if not self.args.create_pass:
            raise ValueError('"Password to create" must be provided')
        create_dn = self._get_dn(self.args.create_user)
        user = self.args.create_user
        passwd = self.args.create_pass
        attrs = dict()
        attrs['objectclass'] = [
            b'top', b'person', b'organizationalPerson', b'user'
        ]
        attrs['cn'] = user.encode()
        attrs['sn'] = user.encode()
        attrs['displayName'] = user.encode()
        attrs['userPassword'] = passwd.encode()
        user_domain = user + '@' + self._get_domain()
        attrs['userPrincipalName'] = user_domain.encode()
        attrs['sAMAccountName'] = user.encode()
        attrs['description'] = b"User created from ARGOS RPA+"
        ldif = modlist.addModlist(attrs)
        self.conn.add_s(create_dn, ldif)
        return self.get(user)

    # ==========================================================================
    def delete(self):
        if not self.isopend:
            print(self.r_conn, end='')
            return False
        if not self.args.delete_user:
            raise ValueError('"User to delete" must be provided')
        delete_dn = self._get_dn(self.args.delete_user)
        self.conn.delete_s(delete_dn)
        self.r_conn = 'deleted'
        print(self.r_conn, end='')


################################################################################
@func_log
def do_ldap(mcxt, argspec):
    """
    plugin job function
    :param mcxt: module context
    :param argspec: argument spec
    :return: True
    """
    mcxt.logger.info('>>>starting...')
    try:
        with LdapOp(argspec) as lo:
            lo.open()
            if argspec.op == 'Get':
                lo.get()
            elif argspec.op == 'Search':
                lo.search()
            elif argspec.op == 'Modify':
                lo.modify()
            elif argspec.op == 'Create':
                lo.create()
            elif argspec.op == 'Delete':
                lo.delete()
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
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
        group='9',  # Utility Tools
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='AD/LDAP',
        icon_path=get_icon_path(__file__),
        description='Active Directory or LDAP opeartion',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--port', '-p',
                          display_name='Port',
                          type=int, default=389,
                          help='Port number default is [[389]]')
        # mcxt.add_argument('--dn',
        #                   display_name='Distinguished Name',
        #                   help='Distinguished Name for Create/Modify/Delete, example [[CN=myuser,CN=Users,DC=ad,DC=vivans,DC=net]]')
        mcxt.add_argument('--search-attributes',
                          display_name='Attributes to search', action='append',
                          help='Searching attributes, example [[name=user*]]')
        mcxt.add_argument('--modify-user',
                          display_name='User to modify',
                          help='User to modify, if omitted logined user instead')
        # mcxt.add_argument('--modify-from',
        #                   display_name='Old Attr to modify',
        #                   help='Modify attribute to find, example [[description=old description]]')
        mcxt.add_argument('--modify-to',
                          display_name='New Attr to modify',
                          help='Modify attribute to modify, example [[description=new description]]')
        mcxt.add_argument('--create-user',
                          display_name='User to create',
                          help='User to create')
        mcxt.add_argument('--create-pass', input_method='password',
                          display_name='Password to create',
                          help='User password to create')
        mcxt.add_argument('--delete-user',
                          display_name='User to delete',
                          help='User to delete')
        # ##################################### for app dependent parameters
        mcxt.add_argument('op',
                          display_name='Operation',
                          default=LdapOp.OP[0],
                          choices=LdapOp.OP,
                          help='AD/LDAP operation for user')
        mcxt.add_argument('host',
                          display_name='Server',
                          help='AD/LDAP host name or ip address')
        mcxt.add_argument('user',
                          display_name='User',
                          help='User to login [[userid@ad.example.com]]')
        mcxt.add_argument('passwd',
                          display_name='Password', input_method='password',
                          help='Password to login')
        argspec = mcxt.parse_args(args)
        return do_ldap(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
