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
import blt_parser
import yaml

#This does not much more than copy files around and set up macro loading
class FreeCADBackend:
	def __init__(self,path):
		self.repo_root = path

		#get application independent data
		self.repo = blt_parser.BOLTSRepository(path)
		self.basefiles = []

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

	def write_output(self):
		out_path = join(self.backend_root,"output")
		bolts_path = join(out_path,"bolts")

		#clear output and copy files
		rmtree(out_path,True)

		makedirs(bolts_path)
		#copy blt files
		copytree(join(self.repo_root,"data"),join(bolts_path,"data"))
		#copy gui stuff
		copytree(join(self.backend_root,"common"),join(bolts_path,"common"))
		for coll,filename in self.basefiles:
			makedirs(join(bolts_path,coll))
			copy(join(self.backend_root,coll,filename),join(bolts_path,coll))

		init_fid = open(join(bolts_path,"__init__.py"),"w")
		init_fid.write("import sys\n")

		#collect bases
		init_fid.write("bases = {}\n")
		for coll,filename in self.basefiles:
			modname = splitext(filename)[0]
			init_fid.write("sys.path.append('bolts/%s')\n" % coll)
			init_fid.write("import %s\n" % modname)
			init_fid.write("bases.update(%s.bases)\n\n" % modname)


		init_fid.write("sys.path.append('bolts/common')\n")
		init_fid.write("from freecad_bolts import BoltsWidget, getMainWindow\n")



