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
from common import DataBase, BaseElement, Parameters, check_schema, Links, BijectiveLinks


class OpenSCADGeometry(BaseElement):
	def __init__(self,basefile,collname):
		BaseElement.__init__(self,basefile)
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
			self.parameters = Parameters(mod["parameters"])
		else:
			self.parameters = Parameters({"types" : {}})

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
	def __init__(self,repo):
		DataBase.__init__(self,"openscad",repo)

		self.bases = []
		self.connectors = []

		self.base_classes = Links()
		self.collection_bases = Links()
		self.base_connectors = BijectiveLinks()

		if not exists(join(self.backend_root)):
			e = MalformedRepositoryError("openscad directory does not exist")
			e.set_repo_path(repo.path)
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
							self.bases.append(module)
							self.collection_bases.add_link(repo.collections[coll],module)

							if "connectors" in mod:
								connectors = Connectors(mod["connectors"])
								self.base_connectors.add_link(module,connectors)

							for id in module.classids:
								if not id in repo.classes:
									raise MalformedBaseError(
										"Unknown class %s" % id)
								if self.base_classes.contains_dst(repo.classes[id]):
									raise NonUniqueBaseError(id)
								self.base_classes.add_link(module,repo.classes[id])
						except ParsingError as e:
							e.set_base(basefile["filename"])
							raise e
				else:
					raise MalformedBaseError("Unknown base type %s" % basefile["type"])
