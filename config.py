#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#
#  Copyright 2013 qiaoliyong <qiaoliyong@localhost.localdomain>
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

import ConfigParser

class config:
	def __init__(self, conf='./conf'):
		self._conf = conf
		self._configparser = ConfigParser.ConfigParser()
		self._configparser.read(self._conf)

	def get(self, var):
		return self._configparser.get('conf', var)

	def get_data(self, var):
		return self._configparser.get('data', var)

	def get_build(self, var):
		return self._configparser.get('build', var)

	def set(self, var, val):
		pass

if __name__ == "__main__":
	conf = config()
	print conf.get('user')
	print conf.get('password')
	print conf.get_data('qemu')
