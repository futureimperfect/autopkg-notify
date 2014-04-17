#!/usr/bin/env python

'''
This post-install script configures AutoPkgNotify.

Created by James Barclay on 2014-04-14.
'''

from __future__ import print_function

import os
import subprocess
import sys
import time

# Constants
AUTOPKG_NOTIFY_LAUNCHD_PATH = '/Library/LaunchDaemons/com.github.futureimperfect.autopkg-notify.plist'

def get_console_user():
    '''Returns the currently logged-in user as
    a string, even if running as EUID root.'''
    if os.geteuid() == 0:
        console_user = subprocess.check_output(['/usr/bin/stat',
                                                '-f%Su',
                                                '/dev/console']).strip()
    else:
        import getpass
        console_user = getpass.getuser()

    return console_user

def is_root():
    '''Returns true if running as the root user.'''
    if os.geteuid() == 0:
        return True

def touch(path):
    '''Mimics the behavior of the `touch`
    command-line utility.'''
    with open(path, 'a'):
        os.utime(path, None)

def main():
    console_user = get_console_user()
    user_log_dir = os.path.expanduser('~%s' % console_user)
    autopkg_notify_stdout_log = os.path.join(user_log_dir, 'Library/Logs/autopkg-notify.log')
    autopkg_notify_stderr_log = os.path.join(user_log_dir, 'Library/Logs/autopkg-notify.log')
    launch_daemon = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">

    <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.github.futureimperfect.autopkg-notify</string>
            <key>Program</key>
            <string>/Library/Application Support/autopkg-notify/autopkg-notify/autopkg_notify.py</string>
            <key>RunAtLoad</key>
            <true/>
            <key>UserName</key>
            <string>%s</string>
            <key>StandardOutPath</key>
            <string>%s</string>
            <key>StandardErrorPath</key>
            <string>%s</string>
            <key>StartCalendarInterval</key>
            <dict>
                <key>Hour</key>
                <integer>3</integer>
                <key>Minute</key>
                <integer>0</integer>
            </dict>
        </dict>
    </plist>''' % (console_user, autopkg_notify_stdout_log, autopkg_notify_stderr_log)

    if not os.path.isdir(user_log_dir):
        os.makedirs(user_log_dir)

    if not os.path.isfile(autopkg_notify_stdout_log):
        touch(autopkg_notify_stdout_log)

    if not os.path.isfile(autopkg_notify_stderr_log):
        touch(autopkg_notify_stderr_log)

    f = open(AUTOPKG_NOTIFY_LAUNCHD_PATH, 'w')
    print(launch_daemon, file=f)
    # Sleep for 5 seconds
    time.sleep(5)
    try:
        subprocess.check_output(['/bin/launchctl',
                                 'load',
                                 '-w',
                                 '%s' % AUTOPKG_NOTIFY_LAUNCHD_PATH])
    except subprocess.CalledProcessError, e:
        print('Encountered an error when loading %s with launchctl. Error: %s.' % (AUTOPKG_NOTIFY_LAUNCHD_PATH, e))

if __name__ == '__main__':
    if not is_root():
        print('This script must run as root. Exiting now.')
        sys.exit(1)
    main()
