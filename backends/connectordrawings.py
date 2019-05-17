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

from common import Backend
from openscad import OpenSCADBackend,get_signature
from errors import *
from os import makedirs
from os.path import join, exists

class ConnectorDrawingsBackend(Backend):
	def __init__(self,repo,databases):
		Backend.__init__(self,repo,"connectordrawings",databases,["openscad","drawings"])

	def write_output(self,out_path,**kwargs):
		args = self.validate_arguments(kwargs)

		#clear output and copy files
		self.clear_output_dir(out_path)

		#export BOLTS for openscad
		OpenSCADBackend(self.repo,self.dbs).write_output(out_path,target_license="GPL 3.0+",version="development")

		#connector drawings
		for coll,cl,module in self.dbs["openscad"].iterclasses(['collection','class','module']):
			#find all locations
			if not self.dbs["openscad"].module_connectors.contains_src(module):
				#if no connector is defined for this base
				continue
			locations = self.dbs["openscad"].module_connectors.get_dst(module).locations

			#collect all locations covered by drawings
			covered = []
			for draw, in self.dbs["drawings"].itercondrawings(filter_classes=cl):
				covered += self.dbs["drawings"].conlocations_condrawings.get_srcs(draw)

			uncovered = set(locations) - set(covered)
			if len(uncovered) == 0:
				continue

			for loc in uncovered:
				if not exists(join(out_path,"scad",coll.id)):
					makedirs(join(out_path,"scad",coll.id))
				fid = open(join(out_path,"scad",coll.id,"%s-%s.scad" % (module.name,loc)),"w")
				fid.write("include <../../BOLTS.scad>\n")
				fid.write("$fn=50;\n")

				params = cl.parameters.union(module.parameters)
				fid.write("%%%s(%s);\n" % (cl.id,get_signature(params)))
				fid.write('show_cs(%s_conn("%s",%s));\n' % (cl.id,loc,get_signature(params)))
				fid.close()
