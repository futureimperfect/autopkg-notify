#!/usr/bin/env python
# encoding: utf-8

'''
cron2launchd.py
.9 beta 1

This script will take a crontab line as input and generate the
basic plist for used with launchd. Its primary feature is to expand
cron's concise notation into an array start interval dictionaries
used by LaunchD.

Usage:

cron2launchd.py -c '*/40 9-16/2 2 5,6 * say "test"' -l com.example.launchd.label > myfile.plist

Created by Preston Holmes on 2009-07-07.
Modified by James Barclay on 2014-05-23.
Copyright (c) 2009 Preston Holmes

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

import plistlib
import sys

from optparse import OptionParser
from crontab import CronItem, CronRange


def product(*args, **kwargs):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwargs.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def get_slice_as_list(cronslice, label):
    '''
    Probes the python-crontab data structure to return
    an exploded form of cron's concise date range
    '''
    if cronslice.render() == '*':
        return []
    parts = []
    for p in cronslice.parts:
        if isinstance(p, int):
            parts.append((label, p))
        else:
            if isinstance(p, CronRange):
                min_ = p.slice.min
                max_ = p.slice.max

                if p.fro > p.slice.min:
                    min_ = p.fro

                if p.to < p.slice.max:
                    max_ = p.to

                r = (range(int(min_), int(max_), int(p.seq)))

                parts.extend([(label, x) for x in r])
    if parts:
        return parts
    else:
        return '*'


def main(argv=None):
    parser = OptionParser()
    parser.add_option(
        '-v',
        '--verbose',
        action='store_true',
        dest='verbose',
        help='display all verbose output',
        default=False
    )
    parser.add_option('-c', '--cron', dest='line')
    parser.add_option('-l', '--label', dest='label')
    parser.add_option(
        '-i',
        '--ignore-spaces',
        action='store_true',
        dest='ignorespaces',
        help='ignore spaces in the command string'
    )
    parser.add_option(
        '-r',
        '--run-at-load',
        action='store_true',
        dest='runatload',
        help='configure the LaunchD to RunAtLoad'
    )
    parser.add_option(
        '-o',
        '--stdout-path',
        dest='stdoutpath',
        help='specify the stdout path for the LaunchD'
    )
    parser.add_option(
        '-e',
        '--stderr-path',
        dest='stderrpath',
        help='specify the stderr path for the LaunchD'
    )
    parser.add_option(
        '-w',
        '--working-dir',
        dest='workingdir',
        help='specify a directory to chdir(2) to before running the job'
    )
    # parser options: metavar, default action: store
    parser.usage = '''
        Convert a cron command line to a LaunchD plist.
    '''
    (options, args) = parser.parse_args()

    if not options.line:
        parser.error('You must supply a crontab style line as input')

    line = options.line

    if options.label:
        item_label = options.label
    else:
        item_label = 'make.me.unique'

    item = CronItem(line)
    calendar_array = []
    plist = {}
    fields = ('Minute', 'Hour', 'Day', 'Month', 'Weekday')
    array_data = []
    # Extract the time options from the crontab object
    for i in range(len(fields)):
        array_data.append(get_slice_as_list(item.slices[i], fields[i]))
    # Remove empty items
    array_data = [x for x in array_data if x]
    array_data.sort()
    # print array_data
    combos = product(*array_data)
    for i in combos:
        calendar_array.append(dict(i))

    plist['Label'] = item_label
    if options.ignorespaces:
        plist['Program'] = item.command.command
    else:
        plist['ProgramArguments'] = item.command.command.split(' ')
    if options.workingdir:
        plist['WorkingDirectory'] = options.workingdir
    if options.runatload:
        plist['RunAtLoad'] = True
    if options.stdoutpath:
        plist['StandardOutPath'] = options.stdoutpath
    if options.stderrpath:
        plist['StandardErrorPath'] = options.stderrpath
    plist['StartCalendarInterval'] = calendar_array

    print plistlib.writePlistToString(plist)


if __name__ == '__main__':
    sys.exit(main())
