#!/usr/bin/python

# This parses the log file and creates a result file for the last few days which can be consumed by the Raspberry Pi Magic Mirror https://github.com/MichMich/MagicMirror

import re

from datetime import timedelta
import dateutil.parser

import json

import platform

# on the logger raspi setup crontab
'''
crontab -e 

* 5 * * * /usr/bin/python /home/hamcam/write_for_mirror.py
'''

# on the Magic Mirror setup this module https://github.com/timdows/MMM-JsonGraph and add a config like below
'''
{
    module: 'MMM-JsonGraph',
    position: 'top_right',
    header: 'Hamsterlytics',
    config: {
        url: 'http://hamcam.local/',
        arrayName: 'data',
        xAxisName: 'miles',
        textValue: 'milesTxt',
        updateInterval: 60000
    }
},
'''

DIAMETER = 0.75

LAP = (3.1416 * DIAMETER)/5280.0

if platform.system() == 'Linux':
    JSON_RESULT = '/var/www/html/index.html'
    FNAME = '/var/log/supervisor/wheel.log'
else:
    JSON_RESULT = '/Users/willo/Projects/hamcam/test.json'
    FNAME = '/Users/willo/Projects/hamcam/wheel.log'


def main():
    l = []

    with open(FNAME, 'r') as f:
        first = f.readline()
        dt = dateutil.parser.parse(first[15:])

        found = 0
        last = 0
        RE = re.compile('%sT(0[1-9]|1[0-9]|2[0-3])(.*)' % ((dt + timedelta(days=found)).date()))

        for n, s in enumerate(f.readlines()):
            if RE.search(s):
                miles = (n-last) * LAP
                ts = (dt + timedelta(days=found)).date()

                RE = re.compile('%sT(0[1-9]|1[0-9]|2[0-3])(.*)' % (ts))

                print('{} {:.1f}'.format(ts + timedelta(days=-1), miles))

                l.append({'milesTxt': '{} {:.1f}'.format(ts + timedelta(days=-1), miles),
                            'miles': miles})

                found += 1

                last = n
        else:
            # last night
            miles = (n-last) * LAP
            #ts = (dt + timedelta(days=found)).date()

            print('{} {:.1f}'.format(ts, miles))

            l.append({'milesTxt': '{}   {:.1f}'.format(ts, miles),
                        'miles': miles})

    with open(JSON_RESULT, 'w') as f:
        json.dump({'data': l[-5:]}, f)

if __name__ == '__main__':
    main()
