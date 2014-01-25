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

from common import check_schema, DataBase, BaseElement, BOLTSParameters
from errors import *

class FreeCADGeometry(BaseElement):
	def __init__(self,basefile,collname,backend_root):
		BaseElement.__init__(self,basefile,collname)
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
			self.parameters = BOLTSParameters(function["parameters"])
		else:
			self.parameters = BOLTSParameters({"types" : {}})

class BaseFcstd(FreeCADGeometry):
	def __init__(self,obj,basefile, collname,backend_root):
		check_schema(basefile,"basefcstd",
			["filename","author","license","type","objects"],
			["source"])
		check_schema(obj,"basefcstd",
			["objectname","classids"],
			["proptoparam","parameters"]
		)

		FreeCADGeometry.__init__(self,basefile,collname,backend_root)
		self.objectname = obj["objectname"]
		self.proptoparam = {self.objectname : {"Label" : "name"}}
		if "proptoparam" in obj:
			self.proptoparam = obj["proptoparam"]
		if "parameters" in obj:
			self.parameters = BOLTSParameters(obj["parameters"])
		else:
			self.parameters = BOLTSParameters({"types" : {}})

		self.classids = obj["classids"]

class FreeCADData(DataBase):
	def __init__(self,path):
		DataBase.__init__(self,"freecad",path)
		self.getbase = {}

		if not exists(path):
			e = MalformedRepositoryError("Repo directory does not exist")
			e.set_repo_path(path)
			raise e
		if not exists(join(self.backend_root)):
			e = MalformedRepositoryError("freecad directory does not exist")
			e.set_repo_path(path)
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
					basepath = join(self.backend_root,coll,"%s.py" % coll)
					if not exists(basepath):
						raise MalformedBaseError("Python module %s does not exist" % basepath)
					for func in basefile["functions"]:
						try:
							function = BaseFunction(func,basefile,coll,self.backend_root)
							for id in func["classids"]:
								if id in self.getbase:
									raise NonUniqueBaseError(id)
								self.getbase[id] = function
						except ParsingError as e:
							e.set_base(basefile["filename"])
							e.set_collection(coll)
							raise e
				elif basefile["type"] == "fcstd":
					basepath = join(self.backend_root,coll,basefile["filename"])
					if not exists(basepath):
						continue
					for obj in basefile["objects"]:
						try:
							fcstd = BaseFcstd(obj,basefile,coll,self.backend_root)
							for id in obj["classids"]:
								if id in self.getbase:
									raise NonUniqueBaseError(id)
								self.getbase[id] = fcstd
						except ParsingError as e:
							e.set_base(basefile["filename"])
							e.set_collection(coll)
							raise e
