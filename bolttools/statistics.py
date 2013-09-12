# Copyright 2012-2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import listdir
from blt_parser import load_collection

class StatisticExporter:
	def __init__(self):
		self.collections = 0
		self.parts = 0
		self.standards = 0
		self.tables = 0
		self.entries = 0

	def add_collection(self,blt):
		self.collections += 1
		for part in blt["parts"]:
			self.parts += 1

			names = part['name']
			if isinstance(names,str):
				names = [names]
			self.standards += len(names)

			if "table" in part.keys():
				self.tables += 1
				table = part["table"]
				self.entries += len(table["columns"])*len(table["data"])

	def summary(self):
		print self.collections, "Collections"
		print self.parts, "Parts"
		print self.standards, "Standards"
		print self.tables, "Tables"
		print self.entries, "Entries"

files = listdir('blt')

exporter = StatisticExporter()
for file in files:
	if file[-4:] == ".blt":
		coll = load_collection(file)
		exporter.add_collection(coll)

exporter.summary()
