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

from .common import check_schema, DataBase, BaseElement, Parameters, Links
from .common import check_iterator_arguments, filter_iterator_items
from .errors import *

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
		self.parameters = Parameters(function.get("parameters",{"types" : {}}))

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
			try:
				base_info = list(yaml.load_all(open(basefilename,"r","utf8"), Loader=yaml.SafeLoader))
				# SafeLoader is not implemented in pyyaml < 5.1
			except AttributeError:
				# this is deprecated for newer pyyaml versions
				base_info = list(yaml.load_all(open(basefilename,"r","utf8")))
			if len(base_info) != 1:
				raise MalformedCollectionError(
					"Not exactly one YAML document found in file %s" % basefilename
				)
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
								if id not in repo.classes:
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

	def iterclasses(self,items=["class"],**kwargs):
		"""
		Iterator over all classes of the repo.

		Possible items to request: class, collection, base
		"""
		check_iterator_arguments(items,"class",["collection","base"],kwargs)

		for cl,coll in self.repo.iterclasses(["class","collection"]):
			its = {"class" : cl, "collection" : coll}
			if self.base_classes.contains_dst(cl):
				its["base"] = self.base_classes.get_src(cl)

				if filter_iterator_items(its,kwargs):
					yield tuple(its[key] for key in items)

	def iterstandards(self,items=["standard"],**kwargs):
		"""
		Iterator over all standards of the repo.

		Possible items to request: standard, multistandard, body, collection, class, base
		"""
		check_iterator_arguments(items,"standard",["multistandard","body", "collection","class","base"],kwargs)

		parent = ["standard","multistandard","body", "collection","class"]
		for tup in self.repo.iterstandards(parent):
			its = dict(zip(parent,tup))
			if self.base_classes.contains_dst(its["class"]):
				its["base"] = self.base_classes.get_src(its["class"])
				if filter_iterator_items(its,kwargs):
					yield tuple(its[key] for key in items)

	def iternames(self,items=["name"],**kwargs):
		"""
		Iterator over all names of the repo.

		Possible items to request: name, multiname, collection, class, base
		"""
		check_iterator_arguments(items,"name",["multiname", "collection","class","base"],kwargs)

		parent = ["name","multiname", "collection","class"]
		for tup in self.repo.iternames(parent):
			its = dict(zip(parent,tup))
			if self.base_classes.contains_dst(its["class"]):
				its["base"] = self.base_classes.get_src(its["class"])
				if filter_iterator_items(its,kwargs):
					yield tuple(its[key] for key in items)

	def iterbases(self,items=["base"],**kwargs):
		"""
		Iterator over all freecad bases of the repo.

		Possible items to request: base, classes, collection
		"""
		check_iterator_arguments(items,"base",["classes", "collection"],kwargs)

		for base in self.bases:
			its = {"base" : base}
			its["collection"] = self.collection_bases.get_src(base)
			its["classes"] = self.base_classes.get_dsts(base)

			if filter_iterator_items(its,kwargs):
				yield tuple(its[key] for key in items)
