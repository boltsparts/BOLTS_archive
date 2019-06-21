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

from errors import *

FREECADPATH = '/usr/lib/freecad/lib/'  # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
try:
	import FreeCAD
	import Part
	import Sketcher
except:
	raise MissingFreeCADError()

from os.path import join
from os import makedirs, remove
from datetime import datetime
import importlib

from common import BackendExporter

import importWebGL


def add_part(base,params,doc):
	if base.type == "function":
		module = importlib.import_module(base.module_name)
		module.__dict__[base.name](params,doc)
	else:
		raise RuntimeError("Unknown base geometry type" % base.type)

class WebGLExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo, databases)
		self.freecad = databases["freecad"]

	def write_output(self,out_path,template):

		revision = int(FreeCAD.Version()[2].split()[0])
		if revision < 3481:
			raise RuntimeError("FreeCAD version too old")

		importWebGL.template = template

		self.clear_output_dir(out_path)

		#Disable writing bytecode to avoid littering the freecad database with pyc files
		write_bytecode = sys.dont_write_bytecode
		sys.dont_write_bytecode = True

		for coll in self.repo.collections:
			#TODO: handle collision with python standard library properly
			if coll.id == "pipes":
				continue
			makedirs(join(out_path,coll.id))
			sys.path.append(join(self.repo.path,"freecad",coll.id))
			for cl in coll.classes_by_ids():
				if cl.id not in self.freecad.getbase:
					continue

				base = self.freecad.getbase[cl.id]

				try:
					parameters = cl.parameters.union(base.parameters)
					params = parameters.collect(parameters.defaults)
				except:
					print(
						"A problem occurred when parameters for {} where collected for {}"
						.format(cl.parameters.defaults, cl.id)
					)
					raise
				params["standard"] = cl.name
				params["name"] = "irrelevant"
				filename = cl.id + ".js"

				doc = FreeCAD.newDocument()
				add_part(base,params,doc)

				#find bounding box
				part = FreeCAD.ActiveDocument.ActiveObject
				bb = part.Shape.BoundBox
				importWebGL.cameraPosition = (2*bb.XMax, 2*bb.YMax, 2*bb.ZMax)
				importWebGL.wireframeStyle = "multimaterial"
				importWebGL.export([part], join(out_path,coll.id,filename))
				FreeCAD.closeDocument(doc.Name)

			sys.path.pop()

		#restore byte code writing
		sys.dont_write_bytecode = write_bytecode
