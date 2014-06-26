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

import yaml
from os import listdir
from os.path import join, exists, basename, splitext
# pylint: disable=W0622
from codecs import open

from common import check_schema, DataBase, BaseElement, Parameters, Links
from errors import *

class FreeCADGeometry(BaseElement):
	def __init__(self,basefile,collname,backend_root):
		BaseElement.__init__(self,basefile)
		self.filename = basefile["filename"]
		self.path = join(backend_root,collname,self.filename)

class BaseFunction(FreeCADGeometry):
	def __init__(self,function,basefile,collname,backend_root):
		check_schema(function,"basefunction",
			["name","classids"],
			["parameters"]
		)
		check_schema(basefile,"basefunction",
			["filename","author","license","type","functions"],
			["source"]
		)

		FreeCADGeometry.__init__(self,basefile,collname,backend_root)
		self.name = function["name"]
		self.classids = function["classids"]
		self.module_name = splitext(basename(self.filename))[0]
		if "parameters" in function:
			self.parameters = Parameters(function["parameters"])
		else:
			self.parameters = Parameters({"types" : {}})

class FreeCADData(DataBase):
	def __init__(self,repo):
		DataBase.__init__(self,"freecad",repo)
		self.bases = []

		self.base_classes = Links()
		self.collection_bases = Links()

		if not exists(self.backend_root):
			e = MalformedRepositoryError("freecad directory does not exist")
			e.set_repo_path(repo.path)
			raise e

		for coll in listdir(self.backend_root):
			basefilename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basefilename):
				#skip directory that is no collection
				continue
			base_info =  list(yaml.load_all(open(basefilename,"r","utf8")))
			if len(base_info) != 1:
				raise MalformedCollectionError(
						"Not exactly one YAML document found in file %s" % basefilename)
			base_info = base_info[0]
			for basefile in base_info:
				if basefile["type"] == "function":
					basepath = join(self.backend_root,coll,basefile["filename"])
					if not exists(basepath):
						raise MalformedBaseError("Python module %s does not exist" % basepath)
					for func in basefile["functions"]:
						try:
							function = BaseFunction(func,basefile,coll,self.backend_root)
							self.bases.append(function)
							self.collection_bases.add_link(repo.collections[coll],function)
							for id in func["classids"]:
								if not id in repo.classes:
									raise MalformedBaseError(
										"Unknown class %s" % id)
								if self.base_classes.contains_dst(repo.classes[id]):
									raise NonUniqueBaseError(id)
								self.base_classes.add_link(function,repo.classes[id])
						except ParsingError as e:
							e.set_base(basefile["filename"])
							e.set_collection(coll)
							raise e
				else:
					raise MalformedBaseError("Unknown base type %s" % basefile["type"])
	def iterclasses(self):
		for cl in self.repo.classes:
			coll = self.repo.collection_classes.get_src(cl)
			if not self.base_classes.contains_dst(cl):
				continue
			base = self.base_classes.get_src(cl)
			yield(coll,cl,base)
