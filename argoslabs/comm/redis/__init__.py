"""
====================================
 :mod:`argoslabs.comm.redis`
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
#  * [2021/03/27]
#     - 그룹에 "8-Storage Solutions" 넣음
#  * [2019/08/13]
#     - starting

################################################################################
import os
import sys
# noinspection PyPackageRequirements
import redis
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class RedisOp(object):
    # ==========================================================================
    OP_LIST = [
        'SET',                  # 0
        'GET',                  # 1
        'LIST-Append',          # 2
        'LIST-Set',             # 3
        'LIST-Get',             # 4
        'LIST-Remove',          # 5
        'LIST-Length',          # 6
        'SET-Add',              # 7
        'SET-Remove',           # 8
        'SET-IsMember',         # 9
        'SET-Length',           # 10
        'HASH-Set',             # 11
        'HASH-Get',             # 12
        'HASH-Delete',          # 13
        'HASH-Exists',          # 14
        'HASH-Length',          # 15
        'QUEUE-Push',           # 16
        'QUEUE-Pop',            # 17
        'QUEUE-Length',         # 18
        'EXIST',                # 19
        'DELETE',               # 20
        # TODO: pub-sub model
        # 'TRIGGER-Publish',      # 19
        # 'TRIGGER-Subscribe',    # 20
    ]

    # ==========================================================================
    def __init__(self, args, logger):
        self.args = args
        self.logger = logger
        # for internals
        self.opened = False
        self.r = None
        self._open()

    # ==========================================================================
    def _open(self):
        if self.opened:
            self._close()
        self.r = redis.Redis(host=self.args.host, port=self.args.port,
                             db=self.args.db, password=self.args.passwd)
        self.opened = True

    # ==========================================================================
    def _close(self):
        if self.opened:
            self.opened = False
            self.r = None

    # ==========================================================================
    def version(self):
        return self.r.execute_command('INFO')['redis_version']

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def print(self, r):
        if isinstance(r, bytes):
            r = r.decode('utf-8')
        elif not isinstance(r, str):
            r = str(r)
        sys.stdout.write(r)
        sys.stdout.flush()
        self.logger.info('[print] "%s"' % r.strip())

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _safe_str(self, r):
        if r is None:
            raise RuntimeError('Invalid None Value!')
        if isinstance(r, bytes):
            r = r.decode('utf-8')
        elif not isinstance(r, str):
            r = str(r)
        return r

    # ==========================================================================
    # noinspection PyBroadException
    def do(self):
        if not self.opened:
            raise RuntimeError('Not opened!')
        if self.args.op not in self.OP_LIST:
            raise RuntimeError('Invalid Operation "%s"' % self.args.op)
        if not self.args.name:
            raise RuntimeError('Invalid Name')
        name = self.args.name
        self.logger.info('do: "%s"...' % self.args.op)
        op_ndx = self.OP_LIST.index(self.args.op)
        params = []
        if self.args.params:
            params = self.args.params
        if op_ndx == 0:  # SET
            if not params:
                raise RuntimeError('Set first Parameter as value')
            self.r.set(name, params[0])
            self.print(params[0])
        elif op_ndx == 1:  # GET
            r = self.r.get(name)
            r = self._safe_str(r)
            self.print(r)
        elif op_ndx == 2:  # LIST-Append
            if not params:
                raise RuntimeError("Insert Values in Parameters to append in the list")
            self.r.rpush(name, *params)
            r = self.r.llen(name)
            self.print(r)
        elif op_ndx == 3:  # LIST-Set
            try:
                cnt = int(params[0])
                val = params[1]
            except Exception:
                raise RuntimeError('Set first Parameter as count int value')
            if not val:
                raise RuntimeError('Set second Parameter as set value in the list')
            _ = self.r.lset(name, cnt, val)
            r = self.r.llen(name)
            self.print('true' if r else 'false')
        elif op_ndx == 4:  # LIST-Get
            rl = []
            for p in params:
                try:
                    r = self.r.lindex(name, int(p))
                    if r is None:
                        raise RuntimeError('Cannot get item from list "%s"' % name)
                    r = self._safe_str(r)
                except ValueError as err:
                    raise RuntimeError('Invalid index "%s": %s' % (p, str(err)))
                except Exception as err:
                    raise RuntimeError('Error to get an item in list: %s' % str(err))
                rl.append(r.strip() if r else '')
            self.print('\n'.join(rl))
        elif op_ndx == 5:  # LIST-Remove
            try:
                cnt = int(params[0])
                rems = params[1:]
            except Exception:
                raise RuntimeError('Set first Parameter as count int value')
            if not rems:
                raise RuntimeError('Set second Parameter and more as the values to delete')
            for rem in rems:
                self.r.lrem(name, cnt, rem)
            r = self.r.llen(name)
            self.print(r)
        elif op_ndx == 6:  # LIST-Length
            r = self.r.llen(name)
            self.print(r)
        elif op_ndx == 7:  # SET-Add
            if not params:
                raise RuntimeError("Specify Values in Parameters to add in the set")
            self.r.sadd(name, *params)
            r = self.r.scard(name)
            self.print(r)
        elif op_ndx == 8:  # SET-Remove
            if not params:
                raise RuntimeError("Specify Values in Parameters to remove in the set")
            self.r.srem(name, *params)
            r = self.r.scard(name)
            self.print(r)
        elif op_ndx == 9:  # SET-IsMember
            if not (params and len(params) == 1):
                raise RuntimeError("Specify Value in Parameters to check a member in the set")
            r = self.r.sismember(name, params[0])
            self.print('true' if r else 'false')
        elif op_ndx == 10:  # SET-Length
            r = self.r.scard(name)
            self.print(r)
        elif op_ndx == 11:  # HASH-Set
            if not (params and len(params) == 2):
                raise RuntimeError("Specify Key & Value in Parameters to add in the hash")
            r = self.r.hset(name, params[0], params[1])
            self.print('true' if r else 'false')
        elif op_ndx == 12:  # HASH-Get
            if not (params and len(params) == 1):
                raise RuntimeError("Specify Key in Parameters to get in the hash")
            r = self.r.hget(name, params[0])
            r = self._safe_str(r)
            self.print(r)
        elif op_ndx == 13:  # HASH-Delete
            if not params:
                raise RuntimeError("Specify Keys in Parameters to delete in the hash")
            r = self.r.hdel(name, *params)
            self.print('true' if r else 'false')
        elif op_ndx == 14:  # HASH-Exists
            if not (params and len(params) == 1):
                raise RuntimeError("Specify Key in Parameters to check existence in the hash")
            r = self.r.hexists(name, params[0])
            self.print('true' if r else 'false')
        elif op_ndx == 15:  # HASH-Length
            r = self.r.hlen(name)
            self.print(r)
        elif op_ndx == 16:  # QUEUE - Push
            if not (params and len(params) == 1):
                raise RuntimeError("Insert Value in Parameters to push in the queue")
            self.r.rpush(name, params[0])
            r = self.r.llen(name)
            self.print(r)
        elif op_ndx == 17:  # QUEUE-Pop
            r = self.r.blpop(name, timeout=int(self.args.timeout))
            if isinstance(r, tuple):
                r = self._safe_str(r[-1])
            else:
                r = self._safe_str(r)
            self.print(r)
        elif op_ndx == 18:  # QUEUE-Length
            r = self.r.llen(name)
            self.print(r)
        elif op_ndx == 19:  # EXIST
            r = self.r.exists(name)
            self.print('true' if r else 'false')
        elif op_ndx == 20:  # DELETE
            r = self.r.delete(name)
            self.print('true' if r else 'false')
        # elif op_ndx == 19:  # TRIGGER-Publish
        #     if not (params and len(params) == 1):
        #         raise RuntimeError("Specify Message in Parameters to publish in the channel")
        #     r = self.r.publish(name, params[0])
        # elif op_ndx == 20:  # TRIGGER-Subscribe
        #     p = self.r.pubsub()
        #     p.subscribe(name)
        else:
            raise RuntimeError('Not Implemented error for "%s"' % self.args.op)
        return 0


################################################################################
@func_log
def do_redis(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        ro = RedisOp(argspec, logger=mcxt.logger)
        return ro.do()
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS-DEMO',
        group='8',  # Storage Solutions
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Bot Collabo',
        icon_path=get_icon_path(__file__),
        description='Shared Storage among Bots for global variables, list, queue, etc.',
    ) as mcxt:
        # ##################################### for app dependent options
        mcxt.add_argument('--port', type=int, default=6379,
                          display_name='Port',
                          help='Port number for the Redis server, default is [[6379]]')
        mcxt.add_argument('--db', type=int, default=0,
                          display_name='DB Index',
                          help='DB number for the Redis server, default is [[0]]')
        mcxt.add_argument('--passwd',
                          display_name='Password', input_method='password',
                          help='Password for the Redis Server')
        mcxt.add_argument('--timeout', type=int, default=0,
                          display_name='QUEUE Timeout',
                          help='QUEUE timeout for the Redis server, default is [[0]] which means wait forever.')
        # ##################################### for app dependent parameters
        mcxt.add_argument('host',
                          display_name='Host',
                          help='Host name or IP address for the Redis server')
        mcxt.add_argument('op',
                          display_name='Operation',
                          choices=RedisOp.OP_LIST,
                          help='Operation in the Redis server')
        mcxt.add_argument('name',
                          display_name='Name',
                          help='Name of key, list, set, hash, channel,...')
        mcxt.add_argument('params',
                          display_name='Parameters', nargs='*',
                          help='Parameters for each operations in Redis server')
        argspec = mcxt.parse_args(args)
        return do_redis(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
