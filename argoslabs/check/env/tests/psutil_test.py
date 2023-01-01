import psutil


################################################################################
class SystemInfo(object):
    # ==========================================================================
    op_list = [
        'cpu percent',
    ]

    # ==========================================================================
    def __init__(self):
        ...

    # ==========================================================================
    def get_cpu_percent(self, percpu=True):
        r = psutil.cpu_percent(percpu=percpu)
        return r

    # ==========================================================================
    def get(self, op):
        if op not in self.op_list:
            raise RuntimeError(f'Cannot find op "{op}"')
        if op == 'cpu percent':
            return self.get_cpu_percent()


################################################################################
if __name__ == '__main__':
    si = SystemInfo()
    print(si.get('cpu percent'))
    