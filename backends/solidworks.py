#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from os import makedirs, listdir
from os.path import join, exists
from shutil import copyfile

import xlwt

from errors import *
from common import BackendExporter

UNITS = {
	"Length (mm)" : " mm",
	"Length (in)" : " in",
	"Number" : "",
	"Bool" : "",
	"Table Index" : "",
	"String" : ""
}

class SolidWorksExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)
		self.solidworks = databases["solidworks"]

	def write_output(self,out_path,version,stable=False):
		self.clear_output_dir(out_path)

		ver_root = join(out_path,version)
		makedirs(ver_root)

		for designtable in self.solidworks.designtables:
			#build class lookup, we need to search for classes by ids
			blt_classes = {}
			for coll in self.repo.collections:
				if not coll.id == designtable.collection:
					continue
				for cl in coll.classes_by_ids():
					if cl.id in blt_classes:
						raise NonUniqueClassIdError(cl.id)
					blt_classes[cl.id] = cl

			#create directories and copy model files
			coll_path = join(ver_root,designtable.collection)
			if not exists(coll_path):
				makedirs(coll_path)
			#check for case
			if not designtable.filename in listdir(join(self.solidworks.backend_root,designtable.collection)):
				raise FileNotFoundError(designtable.filename)
			model_path = join(coll_path,designtable.filename)
			if not exists(model_path):
				copyfile(designtable.path,model_path)

			#create designtable
			workbook = xlwt.Workbook("utf8")
			worksheet = workbook.add_sheet("Sheet1")

			#write column headers
			c = 1
			r = 0
			for pname in designtable.params:
				worksheet.write(r,c,pname)
				c += 1
			for mname in designtable.metadata:
				worksheet.write(r,c,mname)
				c += 1

			#write configurations
			r = 1
			for dtcl in designtable.classes:
				cl = blt_classes[dtcl.classid]
				for free in cl.parameters.common:
					params = cl.parameters.collect(dict(zip(cl.parameters.free,free)))
					types = cl.parameters.types
					name = "undefined"
					if name is None:
						name = cl.naming.get_name(params)
					else:
						name = dtcl.naming.get_name(params)

					c = 0
					worksheet.write(r,c,name)
					c += 1
					
					for pname in designtable.params.values():
						worksheet.write(r,c,str(params[pname]) + UNITS[types[pname]])
						c += 1

					for pname in designtable.metadata.values():
						worksheet.write(r,c,str(params[pname]))
						c += 1

					r += 1

			workbook.save(join(coll_path,designtable.outname))





