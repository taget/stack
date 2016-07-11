#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  stack.py
#  require for usr.list:
#  username: gerrit_id
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
import json
import sys
from datetime import date
from StringIO import StringIO

import util
import sys

from base import base
from usr import user
from config import config

class stackaly(base):
    def __init__(self, start_date, end_date):
        super(stackaly, self).__init__()
        self._base_url = "http://stackalytics.com/api/1.0/stats/modules"
        self._start_date = start_date
        self._end_date = end_date
        # only used for query
        self._ustart_date = str(int(util.date_to_time(start_date)))
        self._uend_date = str(int(util.date_to_time(end_date)))
        self.usr_list = []
        f =  open('./usr.list')
        for s in f.readlines():
            if len(s) > 1:
                u = user(s)
            self.usr_list.append(u)
        self.conn = httplib2.Http()

        self._metric = self._conf.get('metric').split(',')
#        self._project= self._conf.get('project').split(',')
        self._show = self._conf.get('show').split(',')

    def get_metric_for_usr(self, usr, metric="commits"):
        request_options = {'company': 'intel',
                           'project_type': 'all',
                           'start_date': self._ustart_date,
                           'end_date': self._uend_date,
                           'metric': metric,
                           'release': 'all'}

        if not usr.user_name == 'intel':
            request_options.update({'user_id': usr.gerrit_id})

        out_put = ''
        op = util.genreate_options(request_options)
        try:
            out = util.get_companies(self.conn, self._base_url, op)
            out_dict = json.loads(out)
        except Exception as e:
            # we may got 404, not found user
            print e
            out_dict = {u'stats': []}

        sys.stdout.write('.')
        sys.stdout.flush()
        # all_stats = 0
        all_stats = 0
        for it in out_dict['stats']:
            for i in self._show:
                if it.get(i):
                    o = "%s: %s" % (i, it.get(i))
                    out_put = out_put + o + '\t'
            out_put = out_put + '\r\n'
            # add meta for each project, used to summrize all metris of users
            usr.append_meta(metric, it['name'], int(it.get('metric')))
            all_stats += int(it.get('metric'))
        usr.append_meta(metric, 'all', all_stats)
        usr.append_record(metric, out_put)

    def get_aly_for_all_usr(self):
        for u in self.usr_list:
            for m in self._metric:
                self.get_metric_for_usr(u, m)

    def summary(self):
        msg = StringIO()
        msg.write('Summary [%s] - [%s]\r\n' % (self._start_date, self._end_date))
        for u in self.usr_list:
            msg.write('%s\r\n' % u.record)

        msg.write('===Summary from DCS [%s] - [%s]===\r\n' % (self._start_date, self._end_date))

        # fake a user for dcs to compute metric of all member
        dcs_usr = user("dcs: dcs")
        for m in self._metric:
            val = 0
            for u in self.usr_list:
                val += u.metric(m, 'all')
            dcs_usr.append_meta(m, 'all', val)
            msg.write('%s\t\t%s\t\t[%d]\r\n' % (m, 'all', val))
        # summary
        msg.seek(0)
        print msg.read()

    def test(self):
        pass

    def debug(self):
        print self.usr_list

def main():
    start_date = "2011-11-11"
    end_date = None
    if len(sys.argv) > 1:
        start_date = sys.argv[1]
    if len(sys.argv) > 2:
        end_date = sys.argv[2]
    if not end_date:
        end_date = str(date.today())

    s = stackaly(start_date=start_date, end_date=end_date)
    s.get_aly_for_all_usr()
    s.summary()

if __name__ == '__main__':
    main()
