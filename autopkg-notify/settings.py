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
#
# Sample configuration file for AutoPkgNotify

import os

# SMTP CONFIG
SMTP_FROM = 'autopkg-notify@you.com'
SMTP_TO = ['me@me.com', 'you@you.com']
SMTP_PORT = 587
SMTP_SERVER = 'smtp.gmail.com'
SMTP_USER = 'you@you.com'  # Leave blank if auth isn't required, (e.g., '')
SMTP_TLS = True

# LOG CONFIG
LOG_DIR = '/Users/Shared'
LOG_FILE = os.path.join(LOG_DIR, 'autopkg-notify.log')

# PATH TO AUTOPKG RECIPE LIST
RECIPE_LIST = os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'recipe_list'))

# SMTP PASSWORD SETTINGS
# INCLUDE PLAIN TEXT PASSWORD IN P.TXT IF AUTH IS REQUIRED
SMTP_PASS = None
PW = '../p.txt'
if os.path.isfile(PW):
    with open(PW) as f:
        SMTP_PASS = f.read().strip()
