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

from os import listdir,makedirs
from os.path import join, exists, basename,splitext
from shutil import rmtree,copy,copytree
import yaml
import runpy

class FreeCADData:
	def __init__(self,path):
		self.repo_root = path

		self.basefiles = []
		self.getbasename = {}
		self.backend_root = join(path,"freecad")

		print self.backend_root
		print listdir(self.backend_root)

		for coll in listdir(self.backend_root):
			basename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basename):
				#skip directory that is no collection
				continue
			base_info =  list(yaml.load_all(open(basename)))
			if len(base_info) != 1:
				raise MalformedCollectionError(
						"No YAML document found in file %s" % bltname)
			base_info = base_info[0]
			for basefile in base_info:
				base_functions = {}
				if basefile["type"] == "function":
					basepath = join(self.backend_root,"base",coll,"%s.py" % coll)
					if not exists(basepath):
						print "base module described in %s not found: %s" % (basename, basepath)
					for mod in basefile["modules"]:
						for id in mod["ids"]:
							self.getbasename[id] = mod["name"]


#collect bases
#TODO: read base files instead of this fragile heuristic

class FreeCADExporter:
	def write_output(self,repo):

		repo_path = repo.path
		out_path = join(repo_path,"freecad","output")
		bolts_path = join(out_path,"bolts")

		#clear output and copy files
		rmtree(out_path,True)

		makedirs(bolts_path)
		#copy files
		copytree(join(repo_path,"data"),join(bolts_path,"data"))
		copytree(join(repo_path,"bolttools"),join(bolts_path,"bolttools"))
		copytree(join(repo_path,"drawings"),join(bolts_path,"drawings"))
		makedirs(join(bolts_path,"freecad"))
		copytree(join(repo_path,"freecad","base"),join(bolts_path,"freecad","base"))
		copytree(join(repo_path,"freecad","gui"),join(bolts_path,"freecad","gui"))
		open(join(bolts_path,"freecad","__init__.py"),"w").close()

		#generate package __init__.py with proper
		copy(join(repo_path,"freecad","misc","__init__.py"),bolts_path)
