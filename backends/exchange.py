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
	import FreeCAD, Part, Sketcher
except:
	raise MissingFreeCADError()

from os.path import join, exists, basename, splitext, isfile
from os import listdir, makedirs, remove, devnull
from shutil import rmtree
from datetime import datetime
import importlib

from common import BackendExporter
from freecad import FreeCADExporter

def copy_part_recursive(src_obj,dst_doc,srcdstmap):
	# pylint: disable=F0401

	if src_obj.Name in srcdstmap:
		return srcdstmap[src_obj.Name]
	obj_copy = dst_doc.copyObject(src_obj)
	srcdstmap[src_obj.Name] = obj_copy
	for prop_name in src_obj.PropertiesList:
		prop = src_obj.getPropertyByName(prop_name)
		if 'ReadOnly' in src_obj.getTypeOfProperty(prop_name):
			pass
		elif isinstance(prop,tuple) or isinstance(prop,list):
			new_prop = []
			for p_item in prop:
				if isinstance(p_item,Part.Feature):
					new_prop.append(copy_part_recursive(p_item,dst_doc,srcdstmap))
				elif isinstance(p_item,Sketcher.Sketch):
					new_prop.append(dst_doc.copyObject(p_item))
				else:
					new_prop.append(p_item)
			if isinstance(prop,tuple):
				new_prop = tuple(new_prop)
			setattr(obj_copy,prop_name,new_prop)
		elif isinstance(prop,Sketcher.Sketch):
			setattr(obj_copy,prop_name,dst_doc.copyObject(prop))
		elif isinstance(prop,Part.Feature):
			setattr(obj_copy,prop_name,copy_part_recursive(prop,dst_doc,srcdstmap))
		else:
			setattr(obj_copy,prop_name,src_obj.getPropertyByName(prop_name))
	obj_copy.touch()
	return obj_copy


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
		dst_obj = copy_part_recursive(src_obj,doc,srcdstmap)

		#set parameters
		for obj_name,proptoparam in base.proptoparam.iteritems():
			for prop,param in proptoparam.iteritems():
				setattr(srcdstmap[obj_name],prop,params[param])

		#finish presentation
		dst_obj.touch()
		doc.recompute()
		FreeCAD.setActiveDocument(doc.Name)
		FreeCAD.closeDocument(src_doc.Name)


class IGESExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo, databases)
		self.freecad = databases["freecad"]

	def write_output(self,out_path,version,stable=False):
		self.clear_output_dir(out_path)

		ver_root = join(out_path,version)
		makedirs(ver_root)

		#generate version file
		date = datetime.now()
		version_file = open(join(ver_root,"VERSION"),"w")
		version_file.write("%s\n%d-%d-%d\n" %
			(version, date.year, date.month, date.day))
		version_file.close()

		#Disable writing bytecode to avoid littering the freecad database with pyc files
		write_bytecode = sys.dont_write_bytecode
		sys.dont_write_bytecode = True

		for coll in self.repo.collections:
			makedirs(join(ver_root,coll.id))
			sys.path.append(join(self.repo.path,"freecad",coll.id))
			for cl in coll.classes:
				if not cl.id in self.freecad.getbase:
					continue
				if cl.parameters.common is None:
					continue

				base = self.freecad.getbase[cl.id]

				for free in cl.parameters.common:
					params = cl.parameters.collect(dict(zip(cl.parameters.free,free)))
					params["standard"] = cl.name
					name = cl.naming.get_name(params)
					params["name"] = name
					filename = name + ".igs"
					filename = filename.replace(" ","_").replace("/","-")

					doc = FreeCAD.newDocument()

					add_part(base,params,doc)

					shape = None
					if base.type == "function":
						shape = doc.ActiveObject.Shape
					elif base.type == "fcstd":
						shape = doc.getObject(base.objectname).Shape

					shape.exportIges(join(ver_root,coll.id,filename))
					FreeCAD.closeDocument(doc.Name)
			sys.path.pop()

		#restore byte code writing
		sys.dont_write_bytecode = write_bytecode



