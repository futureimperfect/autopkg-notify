#!/usr/bin/env python
#
# AutoPkgNotify - Email notifications for AutoPkg
# Copyright 2014 James Barclay
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import email
import logging
import os
import plistlib
import smtplib
import subprocess

import settings as s


class AutoPkgNotify(object):
    '''
    Runs AutoPkg and sends email notifications
    when new versions of software are available.
    '''
    def __init__(self,
                 smtp_from,
                 smtp_to,
                 smtp_pass,
                 smtp_port,
                 smtp_server,
                 smtp_user,
                 smtp_tls,
                 recipe_list):

        self.smtp_from = smtp_from
        self.smtp_to = smtp_to
        self.smtp_pass = smtp_pass
        self.smtp_port = smtp_port
        self.smtp_server = smtp_server
        self.smtp_user = smtp_user
        self.smtp_tls = smtp_tls
        self.recipe_list = recipe_list

    def logger(self, msg):
        '''
        Logger for AutoPkgNotify.
        '''
        log_dir = s.LOG_DIR
        log_file = s.LOG_FILE

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(processName)s: %(message)s',
                            level=logging.INFO)

        logging.getLogger('AutoPkgNotify')
        logging.info(msg)

    def send_email(self, new_downloads_array):
        '''
        Sends an email notification containing the names and
        versions of software built with AutoPkg.
        '''
        apps = []
        for download in new_downloads_array:
            app = download.get('app')
            apps.append(app)

        subject = '''[AutoPkgNotify] The Following Software is Now Available
                   for Testing (%s)''' % ', '.join(apps)
        message = '''The following software is now available for testing:\n
                  %s''' % '\n'.join(d['app'] + ': ' + d['version'] for d in new_downloads_array)

        # Construct the message
        msg = email.MIMEMultipart.MIMEMultipart()
        body = email.MIMEText.MIMEText(message)
        msg.attach(body)
        msg.add_header('From', self.smtp_from)
        msg.add_header('To', self.smtp_to)
        msg.add_header('Subject', subject)

        try:
            # Send the message
            mailer = smtplib.SMTP(self.smtp_server, int(self.smtp_port))

            if self.smtp_tls:
                mailer.starttls()

            if self.smtp_user and self.smtp_pass:
                mailer.login(self.smtp_user, self.smtp_pass)

            mailer.sendmail(
                self.smtp_from,
                self.smtp_to.split(', '),
                msg.as_string()
            )
            mailer.close()

        except smtplib.SMTPException as e:
            self.logger('Unable to send email. Error: %s.' % e)

    def run_cmd(self, cmd, redirect_stdout=None):
        '''
        Run a command.
        '''
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={'LC_CTYPE': 'en_CA.UTF-8'}
        )
        out, err = p.communicate()
        if err:
            self.logger(
                '''An error occurred when running command %s.
                 Error: %s''' % (cmd, err)
            )
        return out

    def run_autopkg(self):
        '''
        Runs the AutoPkg recipes specified in s.RECIPE_LIST.
        '''
        app = None
        version = None
        report_cmd = [
            '/usr/local/bin/autopkg',
            'run',
            '--report-plist',
            '--recipe-list',
            self.recipe_list
        ]

        # Run AutoPkg
        report_plist = self.run_cmd(report_cmd)

        # Read the report plist
        report = plistlib.readPlistFromString(report_plist)
        new_downloads = report['new_downloads']
        new_packages = report['new_packages']

        # Send an email notification if there are new downloads
        if len(new_downloads) > 0:
            new_downloads_array = []

            for path in new_downloads:
                new_downloads_dict = {}
                app = path.split('/')[-1].split('.')[0]
                new_downloads_dict['app'] = app

                for dct in new_packages:
                    if app.lower() in dct.get('pkg_path').lower() and 'version' in dct:
                        version = dct.get('version')
                        new_downloads_dict['version'] = version
                    else:
                        new_downloads_dict['version'] = 'N/A'

                new_downloads_array.append(new_downloads_dict)

            self.logger(
                '''New software was downloaded. Sending
                 an alert to %s.''' % self.smtp_to
            )
            self.send_email(new_downloads_array)
        else:
            self.logger('Nothing new was downloaded.')


if __name__ == '__main__':
    apn = AutoPkgNotify(s.SMTP_FROM,
                        s.SMTP_TO,
                        s.SMTP_PASS,
                        s.SMTP_PORT,
                        s.SMTP_SERVER,
                        s.SMTP_USER,
                        s.SMTP_TLS,
                        s.RECIPE_LIST)
    apn.run_autopkg()
