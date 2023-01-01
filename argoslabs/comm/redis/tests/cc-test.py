
import redis
from time import sleep
from threading import Thread


def generator(r, qname):
    for i in range(10):
        # sleep(0.1)
        v = 'value-%d' % i
        r.rpush(qname, v)
        # print('[G-%s] pushed "%s"' % (qname, v))


def worker(r, qname):
    while True:
        qr = r.blpop(qname)
        qrv = qr[1].decode('utf-8')
        print('[W-%s] poped "%s"' % (qname, qrv))


def do():
    host = '192.168.1.249'
    r = redis.Redis(host=host)
    qname = 'q01'

    t_g = Thread(target=generator, args=(r, qname))
    t_w = Thread(target=worker, args=(r, qname))
    t_w.start()
    t_g.start()


if __name__ == '__main__':
    do()
