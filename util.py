#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
#  Copyright 2015 Eli Qiao <liyong.qiao@intel.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import httplib2
import socks
from optparse import OptionParser
import datetime
import time
import json
from datetime import date

def get_companies(conn, request_url=None, options=None):

    if not request_url:
        request_url = "http://stackalytics.com/api/1.0/stats/modules"
    if options:
        request_url = request_url + "?" + options
    r, c = conn.request(request_url)
    if r['status'] == '200':
        return c
    else:
        print r
        print c
        return ""
        #TODO
        raise

def formate_out(str_dict):
    pars = ('name', 'id', 'metric')
    for i in pars:
        if str_dict.get(i):
            print "%s: %s" % (i, str_dict.get(i))

def parse_output(str):
    out_dict = json.loads(str)
    for it in out_dict['stats']:
        formate_out(it)

def genreate_options(dict_opts):
    if not dict_opts:
        return ''
    else:
        l = [(x + '=' +  y) for x, y in dict_opts.items()]
        return "&".join(l)


def get_options(options):
    request_options = {}
    # to generate a options dict
    # return : dict with opthions:
    if not options.start_date:
        # todo
        print "require start date"
        raise
        # todo need a default maybe 1 st
    else:
        start_date = int(date_to_time(options.start_date))
        request_options.update({'start_date': str(start_date)})

    if options.end_date:
        end_date = int(date_to_time(options.end_date))
        request_options.update({'end_date': str(end_date)})
    else:
        end_date = None

    if options.release:
        request_options.update({'release': options.release})
    else:
        request_options.update({'release': 'all'})

    if options.metric:
        request_options.update({'metric': options.metric})

    if options.userid:
        request_options.update({'user_id': options.userid})

    return request_options

def main():
    parser = OptionParser()
    parser.add_option("-s", "--start", dest="start_date",
        help="begin date, '%Y-%m-%d'", default=None)
    parser.add_option("-e", "--end", dest="end_date", default=None,
        help="end date,'%Y-%m-%d', default is today")
    parser.add_option("-m", "--metric", dest="metric", default="commits",
        help="metric, commits, marks(reviews), bpc, resolved-bugs, \
              default is commits")
    parser.add_option("-p", "--project", dest="project", default=None,
        help="project, default is nova")
    parser.add_option("-u", "--userid", dest="userid", default=None,
        help="userid, default is None")
    parser.add_option("-r", "--release", dest="release", default=None,
        help="release, default is None")

    (options, args) = parser.parse_args()

    h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP,
                                                      'proxy-mu.intel.com', 911))

    op = get_options(options)
    out = get_companies(h, options=genreate_options(op))
    parse_output(out)


def test_options(op={'1':"11", "2":"22"}):
    print genreate_options(op)

def date_to_time(str_date):
    date_time = datetime.datetime.strptime(str_date, '%Y-%m-%d')
    return time.mktime(date_time.timetuple())

def test_date():
    today = date.today()
    str(today)
    print datetime.strftime()

def test():
    test_options()
    test_date()


if __name__ == '__main__':
    main()
