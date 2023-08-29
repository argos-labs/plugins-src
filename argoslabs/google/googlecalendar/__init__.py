"""
====================================
 :mod:`argoslabs.google.calendar`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS managing google calendar
"""
# Authors
# ===========
#
# * Irene Cho
#
# Change Log
# --------
#
#  * [2020/07/29]
#     - starting

################################################################################
from __future__ import print_function
import sys
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
import warnings


################################################################################
class Calendar(object):
    # ==========================================================================
    OP_TYPE = ['Event List', 'Create Event', 'Delete Event', 'Update Event']

    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.service = None
        if not self.argspec.sendmail:
            self.sendmail = 'none'
        else:
            self.sendmail = 'all'
        self.val = self.argspec.additional_value
        if self.val:
            for i in range(len(self.val)):
                self.val[i] = self.val[i].split(':')
        self.calendarid = self.argspec.calendarid
        self.body = None
        self.events = None
        self.timemin = self.argspec.timemin

    # ==========================================================================
    def read_file(self):
        if self.argspec.token:
            k = self.argspec.token
            if '\n' in k:
                k = k.strip('\n')
            with open(k, 'rb') as token:
                creds = pickle.load(token)
        self.service = build('calendar', 'v3', credentials=creds)
        return self.service

    # ==========================================================================
    def print_result(self):
        if not self.events:
            print('No upcoming events found.', end='')
        lst_ = ['title', 'start', 'event_id']
        sys.stdout.write(",".join(lst_))
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            try:
                title = event['summary']
            except Exception:
                title = 'None'
            lst = [title, start, event['id']]
            sys.stdout.write('\n')
            sys.stdout.write(','.join(lst))

    # ==========================================================================
    def read_event(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        if self.timemin == 'now':
            self.timemin = now
        events_result = self.service.events().list(calendarId=self.calendarid,
                                                   timeMin=self.timemin,
                                                   showDeleted=False,
                                                   maxResults=self.argspec.maxresults,
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        self.events = events_result.get('items', [])
        self.print_result()
        return self.events

    # ==========================================================================
    def create_body(self):
        at_lst = []
        if self.argspec.attendees:
            for i in self.argspec.attendees:
                at_lst.append({'email': i})
        self.body = {
            'summary': self.argspec.summary,
            'start': {
                'dateTime': self.argspec.startime,
                'timeZone': self.argspec.start_timezone
            },
            'end': {
                'dateTime': self.argspec.endtime,
                'timeZone': self.argspec.end_timezone
            },
            'attendees': at_lst}
        if self.val:
            for i in self.val:
                self.body[i[0]] = i[1]
        return self.body

    # ==========================================================================
    def write_event(self):
        self.events = [self.service.events().insert(
            calendarId=self.argspec.calendarid, sendUpdates=self.sendmail,
            body=self.create_body()).execute()]
        self.print_result()
        return 0

    # ==========================================================================
    def delete_event(self):
        try:
            self.service.events().delete(calendarId=self.calendarid,
                                         eventId=self.argspec.event_id).execute()
            print(f'Delete the {self.argspec.event_id} successfully', end='')
        except Exception as e:
            print(str(e), end='')
        return 0

    # ==========================================================================
    def update(self):
        event = self.service.events().get(calendarId=self.calendarid,
                                          eventId=self.argspec.event_id).execute()
        if self.argspec.summary:
            event['summary'] = self.argspec.summary
        if self.argspec.startime:
            event['start']['dateTime'] = self.argspec.startime
        if self.argspec.start_timezone:
            event['start']['timeZone'] = self.argspec.start_timezone
        if self.argspec.endtime:
            event['end']['dateTime'] = self.argspec.endtime
        if self.argspec.end_timezone:
            event['end']['timeZone'] = self.argspec.end_timezone
        at_lst = []
        if self.argspec.attendees:
            for i in self.argspec.attendees:
                at_lst.append({'email': i})
            event['attendees'] = at_lst
        if self.val:
            for i in self.val:
                event[i[0]] = i[1]
        self.events = [self.service.events().update(calendarId=self.calendarid,
                                                    sendUpdates=self.sendmail,
                                                    eventId=event['id'],
                                                    body=event).execute()]
        self.print_result()
        return 0

    # ==========================================================================
    def do(self, op):
        if op == 'Event List':
            self.read_event()
        elif op == 'Create Event':
            self.write_event()
        elif op == 'Delete Event':
            self.delete_event()
        elif op == 'Update Event':
            self.update()


################################################################################
@func_log
def reg_op(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        warnings.simplefilter("ignore", ResourceWarning)
        res = Calendar(argspec)
        try:
            res.read_file()
            res.do(argspec.op)
        except Exception as err:
            sys.stderr.write('%s%s' % (str(err), os.linesep))
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS-DEMO',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Google Calandar',
            icon_path=get_icon_path(__file__),
            description='Managing schedules in Google Calandar',
    ) as mcxt:
        # ##################################### for app dependent parameters
        mcxt.add_argument('op', display_name='Function type',
                          choices=Calendar.OP_TYPE,
                          help='Type of operation')
        mcxt.add_argument('token', display_name='Token.Pickle',
                          help='Token file', show_default=True,
                          input_method='fileread')
        # ######################################## for app dependent options
        mcxt.add_argument('--event_id', display_name='Event Id',
                          help='event id')
        mcxt.add_argument('--calendarid', display_name='Calendar Id',
                          help='Calendar Id', default='primary')
        mcxt.add_argument('--maxresults', display_name='Max Result',
                          help='Calendar Id', default=10, type=int)
        mcxt.add_argument('--timemin', display_name='Time Min',
                          help='Calendar start time')
        mcxt.add_argument('--startime', display_name='Start Time',
                          help='Calendar start time')
        mcxt.add_argument('--start_timezone', display_name='Start Timezone',
                          help='Calendar start timezone',
                          default='America/Los_Angeles')
        mcxt.add_argument('--endtime', display_name='End Time',
                          help='Event start time')
        mcxt.add_argument('--end_timezone', display_name='End Timezone',
                          help='Calendar end timezone',
                          default='America/Los_Angeles')
        mcxt.add_argument('--summary', display_name='Event Title',
                          help='Event Title')
        mcxt.add_argument('--attendees', display_name='Attendees',
                          help='Attendees', action='append')
        mcxt.add_argument('--sendmail', display_name='Send Invitation',
                          help='boolean', default=False, type=bool)
        mcxt.add_argument('--additional_value',
                          display_name='Additional Values',
                          help='add properties', action='append')
        argspec = mcxt.parse_args(args)
        return reg_op(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
