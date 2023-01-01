#!/usr/bin/env python
# coding=utf8


################################################################################
import os
import sys
import copy
import glob
import yaml
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
from argoslabs.demo.argtest import _main as main


################################################################################
G_PARAMS = ['4000', 'y', '50', '0.5', '1.2.3.4', 'tom', 'jerry', 'foo', 'foo']


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    @staticmethod
    def clear():
        flist = (
            'debug.log', 'error.log', 'helloworld.err', 'helloworld.help',
            'helloworld.py.log', 'helloworld.yaml', 'helloworld.yaml2',
            'mylog.log', 'status.log', '__main__.py.log'
        )
        for f in flist:
            if os.path.exists(f):
                os.unlink(f)
        for f in glob.glob('*.log'):
            os.unlink(f)

    # ==========================================================================
    @staticmethod
    def init_wd():
        mdir = os.path.dirname(__file__)
        os.chdir(mdir)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def myInit(self):
        if TU.isFirst:
            TU.isFirst = False
            self.init_wd()
            self.clear()

    # ==========================================================================
    def setUp(self):
        self.myInit()

    # ==========================================================================
    def tearDown(self):
        pass

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0005_help_with_outfile(self):
        helpfile = 'helloworld.help'
        if os.path.exists(helpfile):
            os.unlink(helpfile)
        try:
            sys.stdout.write('\n%s\n' % ('*'*80))
            _ = main('--help')
            self.assertTrue(False)
        except ArgsExit as _:
            self.assertTrue(True)
        try:
            _ = main('--help', '--outfile', helpfile)
            self.assertTrue(False)
        except ArgsExit as _:
            self.assertTrue(os.path.exists(helpfile))

    # ==========================================================================
    def test0010_json_dump(self):
        try:
            # JSON dump (default)
            sys.stdout.write('\n%s\n' % ('*'*80))
            _ = main('--dumpspec')
            self.assertTrue(False)
        except ArgsExit as _:
            self.assertTrue(True)

    # # ==========================================================================
    # def test0020_yaml_dump_with_output_file(self):
    #     try:
    #         # JSON dump
    #         sys.stdout.write('\n%s\n' % ('*'*80))
    #         _ = main('--dumpspec', 'yaml', '--outfile', 'helloworld.yaml')
    #         self.assertTrue(False)
    #     except ArgsExit as e:
    #         sys.stdout.write('\n%s\n' % str(e))
    #         # add for checking input_group, input_method
    #         with open('helloworld.yaml') as ifp:
    #             yd = yaml.load(ifp)
    #             self.assertTrue(yd['display_name'] == 'My Arg Test')
    #             last_opt = yd['options'][-1]
    #             self.assertTrue(last_opt['name'] == 'radio5'
    #                             and last_opt['input_group'] == 'radio=Your Group;default')
    #             param = yd['parameters'][1]
    #             self.assertTrue(param['name'] == 'intparam'
    #                             and param['input_group'] == 'My Group'
    #                             and param['input_method'] == 'my_int')
    #         self.assertTrue(True)

    # ==========================================================================
    def test0030_dump_error(self):
        try:
            # JSON dump
            sys.stdout.write('\n%s\n' % ('*'*80))
            _ = main('--dumpspec', 'xyz', '--outfile', 'helloworld.yaml')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stdout.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0040_normal_call(self):
        r = main(*G_PARAMS)
        self.assertTrue(r)

    # # ==========================================================================
    # def test0050_normal_call_with_input_file(self):
    #     r = main(*G_PARAMS, '--infile', 'helloworld.yaml')
    #     self.assertTrue(r)
    #
    # # ==========================================================================
    # def test0060_normal_call_with_input_output_file(self):
    #     r = main(*G_PARAMS,
    #              '--infile', 'helloworld.yaml',
    #              '--outfile', 'helloworld.yaml2')
    #     self.assertTrue(r)
    #     with open('helloworld.yaml') as ifp:
    #         h1 = ifp.read()
    #     with open('helloworld.yaml2') as ifp:
    #         h2 = ifp.read()
    #     self.assertTrue(h1, h2)

    # ==========================================================================
    def test0070_error(self):
        try:
            _ = main(*G_PARAMS, '-e')  # main('tom', 'jerry', '--error')
            self.assertTrue(False)
        except RuntimeError as e:
            sys.stdout.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0080_error_file(self):
        try:
            _ = main(*G_PARAMS, '--error', '--errfile', 'helloworld.err')
            self.assertTrue(False)
        except RuntimeError as e:
            sys.stdout.write('\n%s\n' % str(e))
            with open('helloworld.err') as ifp:
                es = ifp.read()
            self.assertTrue(es == 'RuntimeError: MyError\noccurs')

    # ==========================================================================
    def test0090_log_file(self):
        if os.path.exists('mylog.log'):
            os.unlink('mylog.log')
        _ = main(*G_PARAMS, '--logfile', 'mylog.log')
        self.assertTrue(os.path.exists('mylog.log'))

    # ==========================================================================
    def test0100_log_file_with_error(self):
        logfile = 'debug.log'
        if os.path.exists(logfile):
            os.unlink(logfile)
        try:
            _ = main(*G_PARAMS, '-e', '--logfile', logfile)
            self.assertTrue(os.path.exists(logfile))
        except RuntimeError as _:
            with open('helloworld.err') as ifp:
                es = ifp.read()
            self.assertTrue(es == 'RuntimeError: MyError\noccurs')

    # ==========================================================================
    def test0110_log_file_with_error_with_loglevel(self):
        logfile = 'error.log'
        if os.path.exists(logfile):
            os.unlink(logfile)
        try:
            _ = main(*G_PARAMS, '-e', '--logfile', logfile,
                     '--loglevel', 'error')
            self.assertTrue(os.path.exists(logfile))
        except RuntimeError as e:
            self.assertTrue(str(e) == 'MyError\noccurs')
            with open('helloworld.err') as ifp:
                es = ifp.read()
            self.assertTrue(es == 'RuntimeError: MyError\noccurs')

    # ==========================================================================
    def test0120_error_invalid_type(self):
        try:
            _ = main(*G_PARAMS, '--steps', 'foo')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_error_min_value(self):
        try:
            _ = main(*G_PARAMS, '--max-loop', 0)
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0140_error_min_value_ni(self):
        try:
            _ = main(*G_PARAMS, '--steps', -1)
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0150_error_max_value(self):
        try:
            _ = main(*G_PARAMS, '--steps', 6)
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            _ = main(*G_PARAMS, '--steps', 3)
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0160_error_str_min_max_value(self):
        _ = main(*G_PARAMS, '--str-verify', 'def')
        self.assertTrue(True)
        try:
            _ = main(*G_PARAMS, '--str-verify', 'cz')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            _ = main(*G_PARAMS, '--str-verify', 'e')
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0170_error_int_min_max_value(self):
        my_params = copy.deepcopy(G_PARAMS)
        try:
            my_params[1] = '40'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            my_params[1] = '51.1'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # argument intparam: invalid int value: '51.1'
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            my_params[1] = '51'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "intparam", "less_eq" validatation error: user input
            # is "51" but rule is "50"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0180_error_float_min_max_value(self):
        my_params = copy.deepcopy(G_PARAMS)
        try:
            my_params[2] = 'abc'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # argument floatparam: invalid float value: 'abc'
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            my_params[2] = '-0.01'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "floatparam", "greater" validatation error: user
            # input is "-0.01" but rule is "0.0"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
        try:
            my_params[2] = '1'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "floatparam", "less" validatation error: user input
            # is "1.0" but rule is "1.0"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0190_error_re(self):
        my_params = copy.deepcopy(G_PARAMS)
        try:
            my_params[3] = '1.2.3.d'
            _ = main(*my_params)
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "ipaddr", "re_match" validatation error: user input
            # is "1.2.3.d" but rule is "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_statfile(self):
        statfile = 'status.log'
        if os.path.exists(statfile):
            os.unlink(statfile)
        try:
            _ = main(*G_PARAMS, '--statfile', statfile, '--steps', '2')
            self.assertTrue(True)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_verbose(self):
        _ = main(*G_PARAMS, '-v')
        self.assertTrue(True)
        _ = main(*G_PARAMS, '-vv')
        self.assertTrue(True)

    # ==========================================================================
    def test0220_append_option(self):
        argspec = main(*G_PARAMS, '-a', 'app1')
        self.assertTrue(argspec.append == ['app1'])
        argspec = main(*G_PARAMS, '-a', 'bb', '--append', 'cc')
        self.assertTrue(argspec.append == ['bb', 'cc'])
        try:
            _ = main(*G_PARAMS, '-a', 'bb', '--append', 'cc', '-a', 'd')
            self.assertTrue(False)
        except ArgsError as e:
            # For Argument "append", "max_value_ni" validatation error: user
            # input is "d" but rule is "d"
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0230_count_option(self):
        argspec = main(*G_PARAMS)
        self.assertTrue(argspec.count == 0)
        argspec = main(*G_PARAMS, '--count')
        self.assertTrue(argspec.count == 1)
        argspec = main(*G_PARAMS, '--count', '-c')
        self.assertTrue(argspec.count == 2)
        argspec = main(*G_PARAMS, '-cccc')
        self.assertTrue(argspec.count == 4)

    # ==========================================================================
    def test0240_choice_option(self):
        argspec = main(*G_PARAMS, '--choice', '4')
        self.assertTrue(argspec.choice == 4)
        try:
            _ = main(*G_PARAMS, '--choice', '2')
            self.assertTrue(False)
        except ArgsError as e:
            # argument --choice: invalid choice: 2 (choose from 3, 4, 5)
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.clear()
        self.assertTrue(True)
