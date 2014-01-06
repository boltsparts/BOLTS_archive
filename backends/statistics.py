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

from common import BackendExporter
import license
from errors import *

class StatisticsExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)
		self.freecad = databases["freecad"]
		self.openscad = databases["openscad"]
		self.drawings = databases["drawings"]

	def write_output(self,out_path):
		pass

	def get_contributors_list(self):
		contributors_names = []
		for coll in self.repo.collections:
			for name in coll.author_names:
				if not name in contributors_names:
					contributors_names.append(name)
		for base in self.freecad.getbase.values():
			for name in base.author_names:
				if not name in contributors_names:
					contributors_names.append(name)
		for base in self.openscad.getbase.values():
			for name in base.author_names:
				if not name in contributors_names:
					contributors_names.append(name)
		return contributors_names


	def get_part_statistics(self):
		stats = {}
		stats["classes"] = 0
		stats["classes_freecad"] = 0
		stats["classes_openscad"] = 0
		stats["drawings"] = 0
		stats["collections"] = 0
		stats["standards"] = 0
		stats["commonconfigurations"] = 0
		for coll in self.repo.collections:
			stats["collections"] += 1
			for cl in coll.classes_by_ids():
				stats["classes"] += 1
				if not cl.standard is None:
					stats["standards"] += len(cl.standard)
			for cl in coll.classes:
				if not cl.parameters.common is None:
					stats["commonconfigurations"] += len(cl.parameters.common)
		stats["bodies"] = len(self.repo.standard_bodies)

		return stats



