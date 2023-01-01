#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.microsoft.teams`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.microsoft.teams import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.tenant=''
        self.client_id=''
        self.username=''
        self.password=''

    # # ==========================================================================
    # def test0100_send_channel_message(self):
    #     try:
    #         r = main('Channel Send Message',
    #                  self.tenant,
    #                  self.client_id,
    #                  self.username,
    #                  self.password,
    #                  '--channel_link',
    #                  'https://teams.microsoft.com/l/channel/19%3a60641d6e5b6f4a138647976950146f78%40thread.tacv2/test?groupId=bc52cf67-0d31-4c5d-bbe4-81c99b59a022&tenantId=222d07ee-1882-4330-b077-4403d760393b',
    #                  # '--team_id','bc52cf67-0d31-4c5d-bbe4-81c99b59a022',
    #                  # '--channel_id','19:60641d6e5b6f4a138647976950146f78@thread.tacv2',
    #                  '--message',"plugin test with file",
    #                  '--file',
    #                  r'C:\Users\Administrator\Pictures\Screenshots\Screenshot (25).png',
    #                  '--file',
    #                  r'C:\Users\Administrator\Documents\data1.csv',
    #                  # ''
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_send_chat_message(self):
    #     try:
    #         r = main('Chat Send Message',
    #                  self.tenant,
    #                  self.client_id,
    #                  self.username,
    #                  self.password,
    #                  '--chat_id',
    #                  '19:19179a13bc8441da8151c741a1f736f8@thread.v2',
    #                  # '19:69d058f9-609f-4655-bfe6-1a06a878d411_7299542a-1697-4ec1-812b-6b70065c0795@unq.gbl.spaces',
    #                  '--message',"plugin test with file",
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_get_user_list(self):
    #     try:
    #         r = main('Get Users List',
    #                  self.tenant,
    #                  self.client_id,
    #                  self.username,
    #                  self.password
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_get_chat_user_list(self):
    #     try:
    #         r = main('Get Chat Members List',
    #                  self.tenant,
    #                  self.client_id,
    #                  self.username,
    #                  self.password,
    #                  '--chat_id',
    #                  '19:19179a13bc8441da8151c741a1f736f8@thread.v2'
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # # ==========================================================================
    # def test0100_get_channel_user_list(self):
    #     try:
    #         r = main('Get Channel Members List',
    #                  self.tenant,
    #                  self.client_id,
    #                  self.username,
    #                  self.password,
    #                  '--channel_link',
    #                  'https://teams.microsoft.com/l/channel/19%3a60641d6e5b6f4a138647976950146f78%40thread.tacv2/test?groupId=bc52cf67-0d31-4c5d-bbe4-81c99b59a022&tenantId=222d07ee-1882-4330-b077-4403d760393b',
    #                  # '--team_id','bc52cf67-0d31-4c5d-bbe4-81c99b59a022',
    #                  # '--channel_id','19:60641d6e5b6f4a138647976950146f78@thread.tacv2',
    #                  )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)
    #
