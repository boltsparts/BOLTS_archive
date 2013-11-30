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

from os import makedirs, remove
from os.path import join, exists, basename
from shutil import copy, move, copytree, copyfile, rmtree
# pylint: disable=W0622
from codecs import open
from datetime import datetime

from common import BackendExporter
import license
from errors import *

class FreeCADExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)
		self.freecad = databases["freecad"]
	def write_output(self,out_path,target_license,version="unstable"):

		self.clear_output_dir(out_path)
		bolts_path = join(out_path,"BOLTS")

		#generate macro
		start_macro = open(join(out_path,"start_bolts.FCMacro"),"w")
		start_macro.write("import BOLTS\n")
		start_macro.close()

		#copy files
		#bolttools
		if not license.is_combinable_with("LGPL 2.1+",target_license):
			raise IncompatibleLicenseError("bolttools licensed under LGPL 2.1+, which is not compatible with %s" % target_license)
		copytree(join(self.repo.path,"bolttools"),join(bolts_path,"bolttools"))
		#remove the .git file, because it confuses git
		remove(join(bolts_path,"bolttools",".git"))
		#remove the test suite and documentation, to save space
		rmtree(join(bolts_path,"bolttools","test"))
		rmtree(join(bolts_path,"bolttools","doc"))

		#generate version file
		date = datetime.now()
		version_file = open(join(bolts_path,"VERSION"),"w")
		version_file.write("%s\n%d-%d-%d\n%s\n" %
			(version, date.year, date.month, date.day, target_license))
		version_file.close()

		#freecad gui code
		if not license.is_combinable_with("LGPL 2.1+",target_license):
			raise IncompatibleLicenseError("FreeCAD gui files are licensed under LGPL 2.1+, which is not compatible with %s" % target_license)
		if not exists(join(bolts_path,"freecad")):
			makedirs(join(bolts_path,"freecad"))
		if not exists(join(bolts_path,"data")):
			makedirs(join(bolts_path,"data"))
		open(join(bolts_path,"freecad","__init__.py"),"w").close()

		copytree(join(self.repo.path,"backends","freecad","gui"),join(bolts_path,"gui"))
		copytree(join(self.repo.path,"backends","freecad","assets"),join(bolts_path,"assets"))
		copytree(join(self.repo.path,"icons"),join(bolts_path,"icons"))
		copyfile(join(self.repo.path,"backends","freecad","init.py"),join(bolts_path,"__init__.py"))
		open(join(bolts_path,"gui","__init__.py"),"w").close()

		for coll in self.repo.collections:
			if not license.is_combinable_with(coll.license_name,target_license):
				continue
			copy(join(self.repo.path,"data","%s.blt" % coll.id),
				join(bolts_path,"data","%s.blt" % coll.id))

			if not exists(join(bolts_path,"freecad",coll.id)):
				makedirs(join(bolts_path,"freecad",coll.id))

			if not exists(join(self.repo.path,"freecad",coll.id,"%s.base" % coll.id)):
				continue

			copy(join(self.repo.path,"freecad",coll.id,"%s.base" % coll.id),
				join(bolts_path,"freecad",coll.id,"%s.base" % coll.id))

			open(join(bolts_path,"freecad",coll.id,"__init__.py"),"w").close()

			for cl in coll.classes:
				base = self.freecad.getbase[cl.id]
				if not base.license_name in license.LICENSES:
					continue
				if not license.is_combinable_with(base.license_name,target_license):
					continue
				copy(join(self.repo.path,"freecad",coll.id,basename(base.filename)),
					join(bolts_path,"freecad",coll.id,basename(base.filename)))
