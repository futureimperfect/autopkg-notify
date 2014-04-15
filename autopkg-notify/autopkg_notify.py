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
import os
import re
import smtplib
import subprocess
import sys

import settings as s

class AutoPkgNotify:
    '''Runs AutoPkg and sends email notifications
    when new versions of software are available.'''
    def __init__(self, smtp_from, smtp_to, smtp_pass, smtp_port, smtp_server, smtp_user, smtp_tls, recipes_to_run):
        self.smtp_from      = smtp_from
        self.smtp_to        = smtp_to
        self.smtp_pass      = smtp_pass
        self.smtp_port      = smtp_port
        self.smtp_server    = smtp_server
        self.smtp_user      = smtp_user
        self.smtp_tls       = smtp_tls
        self.recipes_to_run = recipes_to_run

    def send_email(self, app, version):
        if version:
            subject = '%s Version %s is Available for Testing' % (app, version)
            message = 'Version %s of %s is now available for testing.' % (version, app)
            print('Version %s of %s was processed. Sending email notification to %s.' % (version, app, self.smtp_to))
        else:
            subject = message = 'A new version of %s is available for testing' % app
            print('A new version of %s was processed. Sending email notification to %s.' % (app, self.smtp_to))

        # Construct the message
        msg = email.MIMEMultipart.MIMEMultipart()
        body = email.MIMEText.MIMEText(message)
        msg.attach(body)
        msg.add_header('From', self.smtp_from)
        msg.add_header('To', ', '.join(self.smtp_to))
        msg.add_header('Subject', subject)

        # Send the message
        mailer = smtplib.SMTP(self.smtp_server, self.smtp_port)

        if self.smtp_tls:
            mailer.starttls()

        if self.smtp_user and self.smtp_pass:
            mailer.login(self.smtp_user, self.smtp_pass)

        mailer.sendmail(self.smtp_from, [', '.join(self.smtp_to)], msg.as_string())
        mailer.close()

    def run_autopkg(self):
        for recipe in self.recipes_to_run:
            try:
                output  = subprocess.check_output(['/usr/local/bin/autopkg',
                                                  'run',
                                                  '-v',
                                                  recipe])

                app     = os.path.splitext(recipe)[0]
                lines   = output.split('\n')
                version = None

                if 'Item at URL is unchanged' in output:
                    print('Nothing new was downloaded. Moving on.')

                elif 'Nothing downloaded, packaged or imported' in output:
                    print('Nothing changed. Moving on.')

                elif 'The following new items were downloaded' in output:
                    sparkle_match = [s for s in lines if 'Version retrieved from appcast:' in s]
                    if sparkle_match:
                        version = sparkle_match[0].split(' ')[-1]

                    self.send_email(app, version)

                else:
                    match = [s for s in lines if 'The following ' in s]
                    if match:
                        version_line = lines.index(match[0]) + 3
                        version      = re.split(' +', lines[version_line])[2]

                    self.send_email(app, version)

            except subprocess.CalledProcessError, e:
                print('An error occurred when running the %s recipe. Error: %s' % (recipe, e))

if __name__ == '__main__':
    apn = AutoPkgNotify(s.SMTP_FROM,
                        s.SMTP_TO,
                        s.SMTP_PASS,
                        s.SMTP_PORT,
                        s.SMTP_SERVER,
                        s.SMTP_USER,
                        s.SMTP_TLS,
                        s.RECIPES_TO_RUN)
    apn.run_autopkg()
