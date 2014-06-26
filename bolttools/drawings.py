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

import yaml
from os import listdir
from glob import iglob
from os.path import join, exists, splitext
# pylint: disable=W0622
from codecs import open

from errors import *
from common import BaseElement, DataBase, Parameters, check_schema, Links, BipartiteLinks

class Drawing(BaseElement):
	def __init__(self,basefile,collname,backend_root):
		BaseElement.__init__(self,basefile)
		self.filename = basefile["filename"]
		#TODO: move this out so that collname and backend_root can be dropped
		self.path = join(backend_root,collname,self.filename)

		self.versions = {}
	 	for version in iglob(self.path + ".*"):
			ext = splitext(version)[1][1:]
			self.versions[ext] = version

	def get_png(self):
		if "png" not in self.versions:
			return None
		return self.versions["png"]

	def get_svg(self):
		if "svg" not in self.versions:
			return None
		return self.versions["svg"]

class DrawingDimensions(Drawing):
	def __init__(self,basefile,collname,backend_root):
		check_schema(basefile,"drawing",
			["filename","author","license","type","classids"],
			["source"]
		)
		Drawing.__init__(self,basefile,collname,backend_root)

class DrawingConnectors(Drawing):
	def __init__(self,basefile,collname,backend_root):
		check_schema(basefile,"drawing",
			["filename","author","license","type","classids","location"],
			["source"]
		)
		Drawing.__init__(self,basefile,collname,backend_root)

		self.location = basefile["location"]

class DrawingsData(DataBase):
	def __init__(self,repo):
		DataBase.__init__(self,"drawings", repo)
		self.dimensions = []
		self.connectors = []
		self.locations = []

		self.dimension_classes = Links()
		self.connectors_classes = BipartiteLinks()
		self.locations_connectors = BipartiteLinks()

		self.collection_dimensions = Links()
		self.collection_connectors = Links()

		if not exists(join(self.backend_root)):
			e = MalformedRepositoryError("drawings directory does not exist")
			e.set_repo_path(path)
			raise e

		for coll in listdir(self.backend_root):
			basefilename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basefilename):
				#skip directory that is no collection
				continue
			if coll not in repo.collections:
				raise MalformedRepositoryError(
					"Drawings for unknown collection found: %s " % coll)
					
			base_info =  list(yaml.load_all(open(basefilename,"r","utf8")))
			if len(base_info) != 1:
				raise MalformedCollectionError(
					"Not exactly one YAML document found in file %s" % basefilename)
			base_info = base_info[0]

			for drawing_element in base_info:
				if drawing_element["type"] == "drawing-dimensions":
					draw = DrawingDimensions(drawing_element,coll,self.backend_root)
					self.dimensions.append(draw)

					if drawing_element["classids"] == []:
						raise MalformedBaseError("Drawing with no associated classes found")
					for id in drawing_element["classids"]:
						self.dimension_classes.add_link(draw,self.repo.classes[id])
					self.collection_dimensions.add_link(repo.collections[coll],draw)
				if drawing_element["type"] == "drawing-connector":
					draw = DrawingConnectors(drawing_element,coll,self.backend_root)
					if not draw.location in self.locations:
						self.locations.append(draw.location)
					self.locations_connectors.add_link(draw.location,draw)

					self.connectors.append(draw)
					for id in drawing_element["classids"]:
						self.connectors_classes.add_link(draw,self.repo.classes[id])
					self.collection_connectors.add_link(repo.collections[coll],draw)

	def iterconnectors(self):
		pass
