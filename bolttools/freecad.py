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

class FreeCADData:
	def __init__(self,path):
		self.repo_root = path

		self.basefiles = []
		self.getbase = {}
		self.backend_root = join(path,"freecad")

		for coll in listdir(self.backend_root):
			basename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basename):
				#skip directory that is no collection
				continue
			base =  list(yaml.load_all(open(basename)))
			if len(base) != 1:
				raise MalformedCollectionError(
						"No YAML document found in file %s" % bltname)
			base = base[0]
			for basefile in base:
				if basefile["type"] == "function":
					self.basefiles.append((coll,basefile["filename"]))
				for mod in basefile["modules"]:
					for id in mod["ids"]:
						self.getbase[id] = mod["name"]

class FreeCADExporter:
	def write_output(self,repo):
		pass
#
#		out_path = join(self.backend_root,"output")
#		bolts_path = join(out_path,"bolts")
#
#		#clear output and copy files
#		rmtree(out_path,True)
#
#		makedirs(bolts_path)
#		#copy blt files
#		copytree(join(self.repo_root,"data"),join(bolts_path,"data"))
#		#copy drawings
#		copytree(join(self.repo_root,"drawings"),join(bolts_path,"drawings"))
#		#copy blt parser
#		copy(join(self.repo_root,"bolttools","blt_parser.py"),bolts_path)
#		#copy gui stuff
#		copytree(join(self.backend_root,"common"),join(bolts_path,"common"))
#		open(join(bolts_path,"common","__init__.py"),"w").close()
#		for coll,filename in self.basefiles:
#			makedirs(join(bolts_path,coll))
#			open(join(bolts_path,coll,"__init__.py"),"w").close()
#			copy(join(self.backend_root,coll,filename),join(bolts_path,coll))
#
#		init_fid = open(join(bolts_path,"__init__.py"),"w")
#
#		#collect bases
#		init_fid.write("bases = {}\n")
#		for coll,filename in self.basefiles:
#			modname = splitext(filename)[0]
#			init_fid.write("import %s.%s\n" % (coll,modname))
#			init_fid.write("bases.update(%s.%s.bases)\n" % (coll,modname))
#
#
#		init_fid.write("""
##start gui
#from common.freecad_bolts import addWidget, BoltsWidget, bolts_path
#
#from blt_parser import BOLTSRepository
#
#repo = BOLTSRepository(bolts_path)
#
#widget = BoltsWidget(repo,bases)
#addWidget(widget)
#""")
#
#
