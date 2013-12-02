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

FREECADPATH = '/usr/lib/freecad/lib/' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
try:
	import FreeCAD, Part
except:
	raise MissingFreeCADError()

from os.path import join, exists, basename, splitext, isfile
from os import listdir, makedirs, remove, devnull
from shutil import rmtree
import importlib

from common import BackendExporter
from freecad import FreeCADExporter

def add_part(base,params,doc):
	if base.type == "function":
		module = importlib.import_module(base.module_name)
		module.__dict__[base.name](params,doc)
	elif base.type == "fcstd":
		#copy part to doc
		src_doc = FreeCAD.openDocument(base.path)
		src_obj = src_doc.getObject(base.objectname)
		if src_obj is None:
			raise MalformedBaseError("No object %s found" % base.objectname)
		#maps source name to destination object
		srcdstmap = {}
		dst_obj = self._recursive_copy(src_obj,doc,srcdstmap)

		#set parameters
		for obj_name,proptoparam in base.proptoparam.iteritems():
			for prop,param in proptoparam.iteritems():
				setattr(srcdstmap[obj_name],prop,params[param])

		#finish presentation
		dst_obj.touch()
		doc.recompute()
		FreeCADGui.getDocument(doc.Name).getObject(dst_obj.Name).Visibility = True
		FreeCAD.setActiveDocument(doc.Name)
		FreeCAD.closeDocument(src_doc.Name)


class STEPExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo, databases)
		self.freecad = databases["freecad"]

	def write_output(self,out_path):
		self.clear_output_dir(out_path)

		#Disable writing bytecode to avoid littering the freecad database with pyc files
		write_bytecode = sys.dont_write_bytecode
		sys.dont_write_bytecode = True

		for coll in self.repo.collections:
			makedirs(join(out_path,coll.id))
			sys.path.append(join(self.repo.path,"freecad",coll.id))
			for cl in coll.classes:
				if not cl.id in self.freecad.getbase:
					continue
				base = self.freecad.getbase[cl.id]

				for free in cl.parameters.common:
					params = cl.parameters.collect(dict(zip(cl.parameters.free,free)))
					params["standard"] = cl.name
					name = cl.naming.get_name(params)
					params["name"] = name
					filename = name + ".step"
					filename = filename.replace(" ","_").replace("/","-")

					doc = FreeCAD.newDocument()

					add_part(base,params,doc)

					#merge all solids of a compound, otherwise the step file contains many objects
					obj = doc.ActiveObject
					shape = obj.Shape
					if isinstance(obj.Shape,Part.Compound):
						shape = obj.Shape.Solids[0]
						for sh in obj.Shape.Solids[1:]:
							shape = shape.fuse(sh)

					#TODO: http://forum.freecadweb.org/viewtopic.php?f=10&t=4905&start=10
					shape.exportStep(join(out_path,coll.id,filename))
					FreeCAD.closeDocument(doc.Name)
			sys.path.pop()

		#restore byte code writing
		sys.dont_write_bytecode = write_bytecode



