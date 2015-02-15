#!/usr/bin/env python
#encoding=utf-8

from base import base

class user(base):
    def __init__(self, config):
        super(user, self).__init__()
        self.parse_config(config)
        self._record = {}
        self._meta = {}

    @property
    def user_name(self):
        return self._user_name

    @property
    def gerrit_id(self):
        return self._gerrit_id

    @property
    def record(self):
        out = "[%s] ^_____^" % self._user_name
        for k in self._record:
            o = "%s : ----------\r\n%s " % (k, self._record[k])
            out += '\r\n' + o
        return out

    def metric(self, metric, proj):
        m = self._meta.get(metric)
        if not m:
            return 0
        return m.get(proj, 0)

    def parse_config(self, config):
        self._user_name = config.split(':')[0].strip()
        self._gerrit_id = config.split(':')[1].strip()

    def append_record(self, record_type, record):
        if self._record.get(record_type):
            self._record[record_type] += '\r\n' + record
        else:
            self._record[record_type] = record

    def append_meta(self, metric, proj, val):
        if not self._meta.get(metric):
            self._meta[metric] = {}
        if not self._meta.get(proj):
            self._meta[proj] = metric
        self._meta[metric][proj] = val
    
    def debug(self):
        print "user name [%s]" % self._user_name
        print "gerrit id [%s]" % self._gerrit_id
        print "record [%s]" % self.record
        print "metric [%s]" % self._meta
		
if __name__ == "__main__":

    usr = user("Eli Qiao: taget-9")
    usr.append_record('commit', 'name..')
    usr.append_record('marks', 'naxxx')
    usr.append_meta('reviews', 'nova', 1)
    print usr.metric('reviews', 'nova') 
