"""
====================================
 :mod:`argoslabs.api.openai.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2023/06/11]
#     - Use OpenAI API

################################################################################
import os
import sys
# import csv
from alabs.common.util.vvargs import ArgsError, ArgsExit
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.api.openai import _main as main
from dotenv import dotenv_values

config = dotenv_values('../../../../../.env')


################################################################################
class TU(TestCase):
    # ==========================================================================

    def setUp(self) -> None:
        cwd = os.path.dirname(os.path.abspath(__file__))
        os.chdir(cwd)

    # ==========================================================================
    def test0000_init(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.assertTrue(os.path.abspath(os.getcwd()) == cwd)

    # ==========================================================================
    def test0100_list_model(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'List Models',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_model_info(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Model Info',
                     '--model', 'gpt-4'
                     )
            self.assertTrue(r == 0)

            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Model Info',
                     )
            self.assertTrue(r == 1)

            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Model Info',
                     '--model', 'gpt-999',
                     )
            self.assertTrue(r == 99)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_chat(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Chat',
                     '--model', 'gpt-3.5-turbo',
                     # '--model', 'gpt-4-0613',
                     '--prompt', 'How to use openai api?',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_chat_text_output(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Chat',
                     '--model', 'gpt-3.5-turbo',
                     # '--model', 'gpt-4-0613',
                     '--prompt', 'How to use openai api?',
                     '--text-output',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_chat_text_output_with_messages_yaml(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Chat',
                     '--model', 'gpt-3.5-turbo',
                     # '--model', 'gpt-4-0613',
                     '--messages-yaml', 'messages01.yaml',
                     '--prompt', 'Where was it played?',
                     '--text-output',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_chat_text_output_with_messages_yaml(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Chat',
                     '--model', 'gpt-3.5-turbo',
                     # '--model', 'gpt-4-0613',
                     '--messages-yaml', 'messages02.yaml',
                     '--text-output',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_gen_imgs(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Gen Images',
                     '--prompt', 'tigers playing piano',
                     '--num-imgs', '3',
                     '--img-size', '1024x1024',
                     '--img-prefix', 'tigers_playing_piano_',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_STT(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Speech to Text',
                     '--voice-file', 'gettysburg.wav',
                     '--text-output',
                     )
            self.assertTrue(r == 0)

            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Speech to Text',
                     '--voice-file', 'gettysburg.wav22',
                     '--text-output',
                     )
            self.assertTrue(r == 2)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0180_chat_ref_text_file(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            r = main(config['OPENAI_ORG'],
                     config['OPENAI_API_KEY'],
                     'Chat',
                     '--model', 'gpt-4',
                     '--ref-text-file', 'contract.txt',
                     '--prompt', ' What are the various binding terms in the agreement?',
                     '--text-output',
                     )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
