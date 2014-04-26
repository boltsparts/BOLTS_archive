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

import yaml
from os import listdir
from os.path import join, exists
# pylint: disable=W0622
from codecs import open

from errors import *
from common import DataBase, BaseElement, BOLTSParameters, check_schema


class OpenSCADGeometry(BaseElement):
	def __init__(self,basefile,collname):
		BaseElement.__init__(self,basefile,collname)
		self.filename = basefile["filename"]
		self.path = join(collname,self.filename)
	def get_copy_files(self):
		"Returns the path of the files to copy relative to the backend_root"
		raise NotImplementedError
	def get_include_files(self):
		"Returns the path of the files to copy relative to the base folder in output"
		raise NotImplementedError
	def get_incantation(self,args):
		"Return the incantation of the base that produces the geometry"
		raise NotImplementedError


class BaseModule(OpenSCADGeometry):
	def __init__(self,mod,basefile,collname):
		check_schema(mod,"basemodule",
			["name", "arguments","classids"],
			["parameters","connectors"])
		check_schema(basefile,"basemodule",
			["filename","author","license","type","modules"],
			["source"])

		OpenSCADGeometry.__init__(self,basefile,collname)
		self.name = mod["name"]
		self.arguments = mod["arguments"]
		self.classids = mod["classids"]

		if "parameters" in mod:
			self.parameters = BOLTSParameters(mod["parameters"])
		else:
			self.parameters = BOLTSParameters({"types" : {}})

		self.connectors = None
		if "connectors" in mod:
			self.connectors = Connectors(mod["connectors"])

	def get_copy_files(self):
		return [self.path]
	def get_include_files(self):
		return [self.filename]
	def get_incantation(self,args):
		return "%s(%s)" % (self.name,", ".join(args[arg] for arg in self.arguments))

class Connectors:
	def __init__(self,cs):
		check_schema(cs,"connectors",
			["name","arguments","locations"],
			[])
		self.name = cs["name"]
		self.arguments = cs["arguments"]
		if not "location" in self.arguments:
			raise MissingLocationError(self.arguments)
		self.locations = cs["locations"]

class OpenSCADData(DataBase):
	def __init__(self,path):
		DataBase.__init__(self,"openscad",path)
		#maps class id to base module
		self.getbase = {}

		if not exists(path):
			e = MalformedRepositoryError("Repo directory does not exist")
			e.set_repo_path(path)
			raise e
		if not exists(join(self.backend_root)):
			e = MalformedRepositoryError("openscad directory does not exist")
			e.set_repo_path(path)
			raise e

		for coll in listdir(self.backend_root):
			basefilename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basefilename):
				#skip directory that is no collection
				continue
			base =  list(yaml.load_all(open(basefilename,"r","utf8")))
			if len(base) != 1:
				raise MalformedCollectionError(
						"No YAML document found in file %s" % basefilename)
			base = base[0]
			for basefile in base:
				if basefile["type"] == "module":
					for mod in basefile["modules"]:
						try:
							module = BaseModule(mod,basefile,coll)
							for id in module.classids:
								if id in self.getbase:
									raise NonUniqueBaseError(id)
								self.getbase[id] = module
						except ParsingError as e:
							e.set_base(basefile["filename"])
							raise e
				else:
					raise MalformedBaseError("Unknown base type %s" % basefile["type"])
