import os
import csv
import sys
import json
import yaml
from bs4 import BeautifulSoup


################################################################################
class BSoup(object):
    # ==========================================================================
    def __init__(self, htmlfile, specfile, parser='html.parser', encoding='utf8'):
        if not (htmlfile and os.path.exists(htmlfile)):
            raise RuntimeError('HTML file "%s" not found' % htmlfile)
        if not (specfile and os.path.exists(specfile)):
            raise RuntimeError('Specification file "%s" not found' % specfile)

        self.htmlfile = htmlfile
        self.specfile = specfile
        self.parser = parser
        self.encoding = encoding
        # for internal
        self.soup = None
        self.spec = None
        self.is_opened = False
        # for csv result
        self.header = list()
        self.rows = list()

    # ==========================================================================
    def open(self):
        with open(self.htmlfile, encoding=self.encoding) as ifp:
            hstr = ifp.read()
        self.soup = BeautifulSoup(hstr, self.parser)
        _, ext = os.path.splitext(self.specfile)
        with open(self.specfile, encoding=self.encoding) as ifp:
            if ext.lower().startswith('.js'):  # try to parse as JSON
                self.spec = json.load(ifp)
            elif ext.lower().startswith('.ya'):  # try to parse as YAML
                if yaml.__version__ >= '5.1':
                    self.spec = yaml.load(ifp, Loader=yaml.FullLoader)
                else:
                    self.spec = yaml.load(ifp)
            else:
                raise RuntimeError('Specification file must has extension of {".yaml", ".jsn", ".yaml", "yml"}')
        self.is_opened = True
        return self.is_opened

    # ==========================================================================
    def close(self):
        if self.is_opened:
            self.is_opened = False

    # ==========================================================================
    def _do_csv_columns(self, spec):
        self.header = list()
        if 'columns' not in spec:
            raise RuntimeError('"columns" spec needed in "%s"' % spec)
        for col, colspec in enumerate(spec['columns']):
            if 'header' in colspec:
                self.header.append(colspec['header'])
            else:
                self.header.append('N/A')
            if 'find' not in colspec:
                raise RuntimeError('"find" spec needed in "%s"' % colspec)
            colspeclist = colspec['find']
            taglist = self.soup.find_all(**colspeclist[0])
            if not (taglist and isinstance(taglist, list)):
                continue
            for row, tag in enumerate(taglist):
                for tagspec in colspeclist[1:]:
                    tag = tag.find(**tagspec)
                    if not tag:
                        break
                if not tag:
                    break
                if len(self.rows) <= row:
                    self.rows.append([])
                self.rows[row].append(tag.text.strip())

    # ==========================================================================
    def _print_result(self):
        if self.rows:
            wr = csv.writer(sys.stdout)
            wr.writerow(self.header)
            for row in self.rows:
                wr.writerow(row)
        else:
            if 'no-result' in self.spec:
                print(self.spec['no-result'])
            else:
                print("No Result")

    # ==========================================================================
    def _do_csv(self, spec):
        if 'columns' in spec:
            self._do_csv_columns(spec)
        elif 'or' in spec:
            for colspec in spec.get('or', []):
                self._do_csv_columns(colspec)
                if self.rows:
                    break
        self._print_result()
        return 0 if self.rows else 1

    # ==========================================================================
    def do_parse(self):
        if not self.is_opened:
            raise RuntimeError('First open()')
        if 'csv' in self.spec:
            spec = self.spec.get('csv', {})
            return self._do_csv(spec)
        else:
            raise RuntimeError('Not supported extraction method like {"csv"}')


################################################################################
if __name__ == '__main__':

    hfef_list = (
        ('1.html', 'ext_01.yaml'),
        ('2.html', 'ext_01.yaml'),
        ('3.html', 'ext_01.yaml'),
        ('4.html', 'ext_01.yaml'),
        ('5.html', 'ext_01.yaml'),
        ('6.html', 'ext_02.yaml'),
        ('7.html', 'ext_02.yaml'),
        ('8.html', 'ext_02.yaml'),
        ('9.html', 'ext_02.yaml'),
        ('10.html', 'ext_02.yaml'),
    )

    for hf, ef in hfef_list:
        print('\n%s%s' % (hf, '=' * 100))
        bs = BSoup(hf, ef)
        bs.open()
        bs.do_parse()
