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

from common import BackendData, BackendExporter
from os import listdir,makedirs
from os.path import join, exists, basename,splitext
from shutil import rmtree,copy,copytree
from errors import *
import yaml
import importlib

_freecad_base_specification = {
	"file-function" : (["filename","author","license","type","functions"],[]),
	"file-fcstd" : (["filename","author","license","type","parts"],[]),
	"function" : (["name","classids"],["baseid"]),
	"part" : (["objectlabel"],["baseid"])
}

class FreeCADBase:
	def __init__(self,basefile,collname):
		self.collection = collname
		self.filename = basefile["filename"]
		self.path = join(collname,self.filename)
		self.author = basefile["author"]
		self.license = basefile["license"]
	def add_part(self,params,doc):
		raise NotImplementedError

class BaseFunction(FreeCADBase):
	def __init__(self,function,basefile,collname):
		self._check_conformity(function,basefile)
		FreeCADBase.__init__(self,basefile,collname)
		self.name = function["name"]
		self.baseid = self.name
		if "baseid" in function:
			self.baseid = function["baseid"]
		self.classids = function["classids"]
		self.module_name = splitext(basename(self.filename))[0]
	def _check_conformity(self,function, basefile):
		spec = _freecad_base_specification
		check_dict(function,spec["function"])
		check_dict(basefile,spec["file-function"])
	def add_part(self,params,doc):
		module = importlib.import_module("BOLTS.freecad.%s.%s" % (self.module_name,self.module_name))
		module.__dict__[self.name](params,doc)

class FreeCADData(BackendData):
	def __init__(self,path):
		BackendData.__init__(self,"freecad",path)
		self.getbase = {}

		for coll in listdir(self.backend_root):
			basename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basename):
				#skip directory that is no collection
				continue
			base_info =  list(yaml.load_all(open(basename)))
			if len(base_info) != 1:
				raise MalformedCollectionError(
						"Not exactly one YAML document found in file %s" % bltname)
			base_info = base_info[0]
			for basefile in base_info:
				if basefile["type"] == "function":
					basepath = join(self.backend_root,coll,"%s.py" % coll)
					if not exists(basepath):
						raise MalformedBaseError("Python module %s does not exist" % basepath)
					for func in basefile["functions"]:
						try:
							function = BaseFunction(func,basefile,coll)
							for id in func["classids"]:
								self.getbase[id] = function
						except ParsingError as e:
							e.set_base(basefile["filename"])
							e.set_collection(coll)
							raise e

class FreeCADExporter(BackendExporter):
	def write_output(self,repo):
		freecad = repo.freecad

		repo_path = freecad.repo_root
		out_path = freecad.out_root
		bolts_path = join(out_path,"BOLTS")

		self.clear_output_dir(freecad)

		#generate macro
		start_macro = open(join(out_path,"start_bolts.py"),"w")
		start_macro.write("import BOLTS\n")
		start_macro.close()

		#copy files
		copytree(join(repo_path,"data"),join(bolts_path,"data"))
		copytree(join(repo_path,"bolttools"),join(bolts_path,"bolttools"))
		copytree(join(repo_path,"drawings"),join(bolts_path,"drawings"))
		copytree(join(repo_path,"freecad"),join(bolts_path,"freecad"))
		copy(join(repo_path,"__init__.py"),bolts_path)
