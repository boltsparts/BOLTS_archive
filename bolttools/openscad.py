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


class SCADFile(BaseElement):
	def __init__(self,basefile,collname):
		BaseElement.__init__(self,basefile)
		self.filename = basefile["filename"]
		self.path = join(collname,self.filename)

class SCADModule(BaseElement):
	def __init__(self,mod,basefile,collname):
		check_schema(mod,"basemodule",
			["name", "arguments","classids"],
			["parameters","connectors"])
		check_schema(basefile,"basemodule",
			["filename","author","license","type","modules"],
			["source"])

		BaseElement.__init__(self,basefile)

		self.name = mod["name"]
		self.arguments = mod["arguments"]
		self.classids = mod["classids"]

		if "parameters" in mod:
			self.parameters = Parameters(mod["parameters"])
		else:
			self.parameters = Parameters({"types" : {}})

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

		self.modules = []
		self.scadfiles = []
		self.connectors = []

		self.module_classes = Links()
		self.scadfile_modules = Links()
		self.collection_modules = Links()
		self.module_connectors = BijectiveLinks()

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
				scadfile = SCADFile(basefile,coll)
				if basefile["type"] == "module":
					for mod in basefile["modules"]:
						try:
							module = SCADModule(mod,basefile,coll)
							self.modules.append(module)
							self.collection_modules.add_link(repo.collections[coll],module)
							self.scadfiles.append(scadfile)
							self.scadfile_modules.add_link(scadfile,module)

							if "connectors" in mod:
								connectors = Connectors(mod["connectors"])
								self.module_connectors.add_link(module,connectors)

							for id in module.classids:
								if not id in repo.classes:
									raise MalformedBaseError(
										"Unknown class %s" % id)
								if self.module_classes.contains_dst(repo.classes[id]):
									raise NonUniqueBaseError(id)
								self.module_classes.add_link(module,repo.classes[id])
						except ParsingError as e:
							e.set_base(basefile["filename"])
							raise e
				else:
					raise MalformedBaseError("Unknown base type %s" % basefile["type"])

	def iterclasses(self):
		for cl in self.repo.classes.values():
			coll = self.repo.collection_classes.get_src(cl)
			if self.module_classes.contains_dst(cl):
				module = self.module_classes.get_src(cl)
				yield(coll,cl,module)

	def itermodules(self,cl=None,coll=None):
		if not cl is None:
			if self.module_classes.contains_dst(cl):
				for module in self.module_classes.get_dsts(cl):
					coll = self.collection_modules.get_src(module)
					classes = self.module_classes.get_dsts(module)
					yield (coll,classes,module)
		elif not coll is None:
			if self.collection_modules.contains_src(coll):
				for module in self.collection_modules.get_dsts(coll):
					classes = self.module_classes.get_dsts(module)
					yield (coll,classes,module)
		else:
			for module in self.modules:
				coll = self.collection_modules.get_src(module)
				classes = self.module_classes.get_dsts(module)
				yield (coll,classes,module)
