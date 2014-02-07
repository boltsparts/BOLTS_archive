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

from common import BackendExporter
from openscad import OpenSCADExporter,get_signature
from errors import *
from os import makedirs
from os.path import join, exists

class ConnectorDrawingsExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)
		self.dbs = databases

	def write_output(self,out_path):
		#clear output and copy files
		self.clear_output_dir(out_path)

		#export BOLTS for openscad
		OpenSCADExporter(self.repo,self.dbs).write_output(out_path,"GPL 3.0+","development")

		#find missing connector drawings
		for coll in self.repo.collections:
			modules = []
			for cl in coll.classes_by_ids():
				if cl.id in self.dbs["openscad"].getbase:
					base = self.dbs["openscad"].getbase[cl.id]
					if base.name in modules:
						continue

					#find all locations
					locations = []
					if base.type == "module" and not base.connectors is None:
						locations = base.connectors.locations

					covered = []
					if cl.id in self.dbs["drawings"].getconnectors:
						for loc in self.dbs["drawings"].getconnectors[cl.id]:
							covered.append(loc)
					uncovered = set(locations) - set(covered)

					for loc in uncovered:
						if not exists(join(out_path,"scad",coll.id)):
							makedirs(join(out_path,"scad",coll.id))
						fid = open(join(out_path,"scad",coll.id,"%s-%s.scad" % (base.name,loc)),"w")
						fid.write("include <../../BOLTS.scad>\n")
						fid.write("$fn=50;\n")
						fid.write("%%%s(%s);\n" %
							(cl.openscadname,get_signature(cl,cl.parameters.union(base.parameters)))
						)
						fid.write('show_cs(%s_conn("%s",%s));\n' %
							(cl.openscadname,loc,get_signature(cl,cl.parameters.union(base.parameters)))
						)
						fid.close()

					modules.append(base.name)

		
