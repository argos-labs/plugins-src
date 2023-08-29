"""
====================================
 :mod:`argoslabs.python.dynamic.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/01/12]
#     - Poh의 pdfplumber 관련 오류 디버그
#  * [2021/07/01]
#     - ASJ의 pywinauto 모듈이 안되는 문제 때문에 exec(py_script, locals(), locals()) 로 수정
#  * [2021/03/30]
#     - starting

################################################################################
import os
import sys
import csv
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.python.dynamic import _main as main

from contextlib import contextmanager
from io import StringIO


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        mdir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(mdir)

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_hello_01(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'hello-01.py'
            with captured_output() as (out, err):
                r = main(pyf)
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out.startswith('Hello World!') and
                            _out.endswith('Dynamic_Python'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_hello_02(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'hello-02.py'
            with captured_output() as (out, err):
                r = main(pyf, '--params', 'name::=Jerry')
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == 'Hello Jerry!')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_add_02(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'add-03.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--params', 'i::=123',
                    '--params', 'j::=10',
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == '133')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_task_1(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'task1.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'requirements.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(os.path.join(
                os.getcwd(), 'task1.xlsx'
            )))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_task_1_err_req(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            pyf = 'task1.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'req-err.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 99)
            _err = err.getvalue()
            self.assertTrue(_err == 'Error: pip install with "req-err.txt" failure!')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_task_2(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'task2.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', 'requirements.txt',
                    '--params', 'wdir::=%s' % os.getcwd(),
                )
            self.assertTrue(r == 0)
            _out = out.getvalue()
            self.assertTrue(_out == os.path.abspath(os.path.join(
                os.getcwd(), 'task2.xlsx'
            )))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # 2021/07/01 수정하고 나서 160과 170을 같이 돌리면 오류 발생: 실제는 괜찮음
    # # ==========================================================================
    # def test0160_scrapy_mike(self):
    #     try:
    #         sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
    #         if sg is None:  # Not in debug mode
    #             print('Skip testing at test/build time')
    #             return
    #         #pyf = 'Webscrape_Argos_Jerry.py'
    #         pyf = 'scrape.py'
    #         odir = os.path.join(os.path.abspath('.'), 'output')
    #         with captured_output() as (out, err):
    #             r = main(
    #                 pyf,
    #                 '--reqtxt', 'req-scrapy.txt',
    #                 '--params', 'searches::=["machine learning", "brain", "food", "robot"]',
    #                 '--params', 'input::=companies-10.csv',
    #                 '--params', f'output_folder::={odir}'
    #             )
    #         self.assertTrue(r == 0)
    #         _out = out.getvalue()
    #         out.seek(0)
    #         rows = list()
    #         cr = csv.reader(out)
    #         for row in cr:
    #             rows.append(row)
    #             self.assertTrue(len(row) in (4,))
    #         self.assertTrue(rows[-1][1] in
    #                             (
    #                                 'https://www.vicarious.com/',
    #                                 'https://misorobotics.com/',
    #                                 'https://dexterity.ai/',
    #                                 'https://sightmachine.com/',
    #                                 'https://www.vicarious.com/',
    #                                 'https://elementaryml.com/',
    #                              )
    #                         )
    #
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test0170_scrapy_mike(self):
    #     try:
    #         sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
    #         if sg is None:  # Not in debug mode
    #             print('Skip testing at test/build time')
    #             return
    #         pyf = 'Webscrape_Argos_Jerry.py'
    #         odir = os.path.join(os.path.abspath('.'), 'output')
    #         with captured_output() as (out, err):
    #             r = main(
    #                 pyf,
    #                 '--reqtxt', r'W:\ARGOS-LABS\Bots\DynamicPythonScrapyMike\req-scrapy.txt',
    #                 '--params', "searches::=['machine learning', 'brain', 'food', 'robot']",
    #                 '--params', r'input::=W:\ARGOS-LABS\Bots\DynamicPythonScrapyMike\companies-10.csv',
    #                 '--params', f'output_folder::=C:\Temp\output'
    #             )
    #         self.assertTrue(r == 0)
    #         csv_f = out.getvalue()
    #         with open(csv_f, encoding='utf-8') as ifp:
    #             rows = list()
    #             cr = csv.reader(ifp)
    #             for row in cr:
    #                 rows.append(row)
    #                 self.assertTrue(len(row) in (4,))
    #             self.assertTrue(rows[-1][1] in
    #                             (
    #                                 'https://www.vicarious.com/',
    #                                 'https://misorobotics.com/',
    #                                 'https://dexterity.ai/',
    #                                 'https://sightmachine.com/',
    #                                 'https://www.vicarious.com/',
    #                                 'https://elementaryml.com/',
    #                             )
    #                             )
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    # def test0180_asj_pywinauto(self):
    #     try:
    #         sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
    #         if sg is None:  # Not in debug mode
    #             print('Skip testing at test/build time')
    #             return
    #         pyf = 'pywinauto_test.py'
    #         odir = os.path.join(os.path.abspath('.'), 'output')
    #         with captured_output() as (out, err):
    #             r = main(
    #                 pyf,
    #                 '--reqtxt', r'pywinauto_reqs.txt',
    #             )
    #         self.assertTrue(r == 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0190_poh_pyplumber_debug(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'dp_pdfplumber.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', r'dp_pdfplumber.txt',
                )
            self.assertTrue(r == 0)
            stdout = out.getvalue()
            self.assertTrue(stdout == '0.6.0')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_python24_test01_error(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'dp_pdfplumber.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--reqtxt', r'dp_pdfplumber.txt',
                    '--python-exe', r'C:\Python24\python.exe',
                )
            self.assertTrue(r == 99)
            stderr = err.getvalue()
            self.assertTrue(stderr.startswith('Error: Cannot install'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0210_python24_test01(self):
    #     try:
    #         # sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
    #         # if sg is None:  # Not in debug mode
    #         #     print('Skip testing at test/build time')
    #         #     return
    #         pyf = 'hello-24.py'
    #         with captured_output() as (out, err):
    #             r = main(
    #                 pyf,
    #                 '--params', r'name::=Jerry',
    #                 '--python-exe', r'C:\Python24\python.exe',
    #             )
    #         self.assertTrue(r == 0)
    #         stdout = out.getvalue()
    #         stderr = err.getvalue()
    #         print(f'stdout="{stdout}"')
    #         print(f'stderr="{stderr}"')
    #         self.assertTrue(stdout.find('Jerry') > 0)
    #     except Exception as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0220_modimp(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'modimp.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--params', 'i::=Hello ',
                    '--params', 'j::=Jerry',
                )
            stdout = out.getvalue()
            print(f'stdout={stdout}')
            stderr = err.getvalue()
            print(f'stderr={stderr}')
            self.assertTrue(r == 0)
            self.assertTrue(stdout.endswith('"Hello Jerry"'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_modimp_from_package(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'modpkg.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--params', 'i::=Hello ',
                    '--params', 'j::=Jerry',
                    '--pythonpath', 'modules',
                )
            stdout = out.getvalue()
            print(f'stdout={stdout}')
            stderr = err.getvalue()
            print(f'stderr={stderr}')
            self.assertTrue(r == 0)
            self.assertTrue(stdout.endswith('"Hello Jerry"'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_flasystem_11st(self):
        try:
            sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
            if sg is None:  # Not in debug mode
                print('Skip testing at test/build time')
                return
            pyf = 'Fla-11st/11st.py'
            with captured_output() as (out, err):
                r = main(
                    pyf,
                    '--params', 'yaml_f::=Fla-11st/11st.yml',
                    '--reqtxt', r'requirements.txt',
                )
            stdout = out.getvalue()
            print(f'stdout={stdout}')
            stderr = err.getvalue()
            print(f'stderr={stderr}')
            self.assertTrue(r == 0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
