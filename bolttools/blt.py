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
import string
import os
from os.path import splitext, exists, join
# pylint: disable=W0622
from codecs import open

from errors import *
from common import Links, Parameters, Identifier, Substitution, parse_angled, check_schema

CURRENT_VERSION = 0.4


class Designation:
	"""
	Base class for python classes to refer to a BOLTS class.
	"""
	def __init__(self):
		pass
	def get_id(self):
		raise NotImplementedError

class ClassName(Designation):
	"""
	Python class to provide a name for a BOLTS class, corresponding to a
	ClassNameElement in the blt file.
	"""
	def __init__(self,cn):
		check_schema(cn,"classname",
			["name","labeling"],
			["description","group"]
		)
		Designation.__init__(self)

		try:
			if isinstance(cn['name'],str):
				self.name = Identifier({'nice' : cn['name']})
			else:
				self.name = Identifier(cn['name'])
			if isinstance(cn['labeling'],str):
				self.labeling = Substitution({'nice' : cn['labeling']})
			else:
				self.labeling = Substitution(cn['labeling'])
		except ParsingError as e:
			e.set_class(self.id)
			raise e

		self.description = ''
		if 'description' in cn:
			self.description = cn['description']

		if 'group' in cn:
			if isinstance(cn['group'],str):
				self.group = Identifier({'nice' : cn['group']})
			else:
				self.group = Identifier(cn['group'])
		else:
			self.group = Identifier({'nice' : ""})

	def get_id(self):
		if self.group.get_safe_name():
			return self.group.get_safe_name() + "_" + self.name.get_safe_name()
		else:
			return self.name.get_safe_name()


class ClassStandard(Designation):
	"""
	Python class to provide a standard name for a BOLTS class, corresponding to a
	ClassStandardElement in the blt file.
	"""
	def __init__(self,sn):
		check_schema(sn,'classstandard',
			['standard','labeling','body'],
			['suffix','year','status','replaces','description']
		)
		Designation.__init__(self)

		if isinstance(sn['standard'],str):
			self.standard = Identifier({'nice' : sn['standard']})
		else:
			self.standard = Identifier(sn['standard'])
		if 'suffix' in sn:
			if isinstance(sn['suffix'],str):
				self.suffix = Identifier({'nice' : sn['suffix']})
			else:
				self.suffix = Identifier(sn['suffix'])
		else:
			self.suffix = Identifier({'nice' : ""})
		if isinstance(sn['labeling'],str):
			self.labeling = Substitution({'nice' : sn['labeling']})
		else:
			self.labeling = Substitution(sn['labeling'])

		self.body = sn['body']
		self.year = None
		if 'year' in sn:
			self.year = sn['year']
		self.status = "active"
		if 'status' in sn:
			self.status = sn['status']
		self.replacedby = None
		self.replaces = None
		if 'replaces' in sn:
			self.replaces = sn['replaces']
		self.description = ""
		if 'description' in sn:
			self.description = sn['description']

	def get_id(self):
		if self.suffix.get_safe_name():
			return self.standard.get_safe_name() + '_' + self.suffix.get_safe_name()
		else:
			return self.standard.get_safe_name()

class Class:
	"""
	Python class representing a BOLTS class. There is no direct
	correspondance between a class in the blt file and this python class,
	some aspects are covered by other classes
	"""
	def __init__(self,cl):
		check_schema(cl,"class",
			["source","id"],
			["names","standards","parameters","url","notes"]
		)

		self.id = cl["id"]

		try:
			if "parameters" in cl:
				self.parameters = Parameters(cl["parameters"])
			else:
				self.parameters = Parameters({"types" : {}})
		except ParsingError as e:
			e.set_class(self.id)
			raise e

		self.url = ""
		if "url" in cl:
			self.url = cl["url"]

		self.notes = ""
		if "notes" in cl:
			self.notes = cl["notes"]

		self.source = cl["source"]


class Collection:
	"""
	Container for all classes contained in a BOLTS Collection
	"""
	def __init__(self,coll):
		check_schema(coll,"collection",
			["id","author","license","blt-version","classes"],
			["name","description"]
		)

		version = coll["blt-version"]
		if version != CURRENT_VERSION:
			raise VersionError(version)

		self.id = coll["id"]

		self.name = ""
		if "name" in coll:
			self.name = coll["name"]

		self.description = ""
		if "description" in coll:
			self.description = coll["description"]

		self.authors = coll["author"]
		if isinstance(self.authors,str):
			self.authors = [self.authors]

		self.author_names = []
		self.author_mails = []
		for author in self.authors:
			match = parse_angled(author)
			self.author_names.append(match[0])
			self.author_mails.append(match[1])

		self.license = coll["license"]
		match = parse_angled(self.license)
		self.license_name = match[0]
		self.license_url = match[1]

class StandardBody:
	"""
	Container for standard names that are specified by a common
	standardisation body
	"""
	def __init__(self,body):
		self.body = body

class MultiStandard(Designation):
	"""
	Container for all standard names that are covered by a single standard
	"""
	def __init__(self,standard):
		Designation.__init__(self)

		self.standard = standard

	def get_id(self):
		return self.standard.get_safe_name()

class MultiName(Designation):
	"""
	Container for class names that are closely related, e.g. variations of a part
	"""
	def __init__(self,group):
		Designation.__init__(self)

		self.group = group
	def get_id(self):
		return self.group.get_safe_name()

class Repository:
	def __init__(self,path):
		#check for conformity
		if not exists(path):
			e = MalformedRepositoryError("Repo directory does not exist")
			e.set_repo_path(path)
			raise e
		if not exists(join(path,"data")):
			e = MalformedRepositoryError("No data directory found")
			e.set_repo_path(path)
			raise e

		self.path = path

		#objects that have an id
		self.classes = {}
		self.collections = {}
		self.names = {}
		self.standards = {}
		self.multinames = {}
		self.multistandards = {}
		self.bodies = {}

		#relations
		self.class_names = Links()
		self.class_standards = Links()
		self.multiname_names = Links()
		self.multistandard_standards = Links()
		self.body_standards = Links()
		self.body_multistandards = Links()
		self.collection_classes = Links()
		self.collection_standards = Links()
		self.collection_multistandards = Links()
		self.collection_names = Links()
		self.collection_multinames = Links()
		self.standard_replaced = Links(1)

		#load collection data
		for filename in os.listdir(join(path,"data")):
			if splitext(filename)[1] != ".blt":
				continue

			raw_coll = list(yaml.load_all(open(join(path,"data",filename),"r","utf8")))
			if len(raw_coll) == 0:
				raise MalformedCollectionError(
						"No YAML document found in file %s" % filename)
			if len(raw_coll) > 1:
				raise MalformedCollectionError(
						"More than one YAML document found in file %s" % filename)
			#we only consider the first YAML document
			raw_coll = raw_coll[0]

			if not isinstance(raw_coll["classes"],list):
				raise MalformedCollectionError("No class in collection %s"% raw_coll["id"])

			if raw_coll["id"] in self.collections:
				raise MalformedCollectionError("Duplicate collection id %s" % raw_coll["id"])

			if raw_coll["id"] != splitext(filename)[0]:
				raise MalformedCollectionError(
					"Collection ID is not identical with file name: %s" % filename)
			for c in raw_coll["id"]:
				if not c in string.ascii_letters +  string.digits + "_":
					raise MalformedCollectionError(
						"Collection ID contains invalid character: %s" % c)

			try:
				coll = Collection(raw_coll)
				self.collections[coll.id] = coll
			except ParsingError as e:
				e.set_repo_path(path)
				e.set_collection(filename)
				raise e

			for cl in raw_coll['classes']:

				if cl["id"] in self.classes:
					raise MalformedRepositoryError("Duplicate class id %s" % cl["id"])

				try:
					cls = Class(cl)
					self.classes[cls.id] = cls
				except ParsingError as e:
					e.set_class(cl["id"])
					e.set_repo_path(path)
					e.set_collection(filename)
					raise e

				self.collection_classes.add_link(coll,cls)

				names = []
				standards = []
				if 'names' in cl:
					if isinstance(cl['names'],list):
						names = cl['names']
					else:
						names = [cl['names']]
				if 'standards' in cl:
					if isinstance(cl['standards'],list):
						standards = cl['standards']
					else:
						standards = [cl['standards']]

				if len(names+standards) == 0:
					raise MalformedCollectionError(
						"Encountered class with no names: %s" % raw_coll["id"])

				for cn in names:
					try:
						name = ClassName(cn)
					except ParsingError as e:
						e.set_class(cls.id)
						raise e
					if name.get_id() in self.names:
						raise MalformedRepositoryError("Duplicate name %s" % name.get_id())

					self.names[name.get_id()] = name
					self.class_names.add_link(cls,name)

					multinameid = name.group.get_safe_name()
					if multinameid:
						if not multinameid in self.multinames:
							multiname = MultiName(name.group)
							self.multinames[multinameid] = multiname
						else:
							multiname = self.multinames[multinameid]
						self.collection_multinames.add_link(coll,multiname)
						self.multiname_names.add_link(multiname,name)
					else:
						self.collection_names.add_link(coll,name)

				for sn in standards:
					try:
						standard = ClassStandard(sn)
					except ParsingError as e:
						e.set_class(cls.id)
						raise e

					if standard.get_id() in self.standards:
						raise MalformedRepositoryError("Duplicate standard %s" % standard.get_id())

					self.standards[standard.get_id()] = standard
					self.class_standards.add_link(cls,standard)

					bodyid = standard.body
					if bodyid in self.bodies:
						body = self.bodies[bodyid]
					else:
						body = StandardBody(bodyid)
						self.bodies[bodyid] = body

					multistdid = standard.suffix.get_safe_name()
					if multistdid:
						if not multistdid in self.multistandards:
							multistd = MultiStandard(standard.standard)
							self.multistandards[multistdid] = multistd
							self.body_multistandards.add_link(body,multistd)
							self.collection_multistandards.add_link(coll,multistd)
						else:
							multistd = self.multistandards[multistdid]

						self.multistandard_standards.add_link(multistd,standard)
					else:
						self.body_standards.add_link(body,standard)

						self.collection_standards.add_link(coll,standard)

		for standard in self.standards.values():
			if not standard.replaces is None:
				if not standard.replaces in self.standards:
					raise MalformedRepositoryError(
						"Unknown replace field %s in standard %s" %
							(standard.replaces,standard.get_id()))
				self.standard_replaced.add_link(standard,self.standards[standard.replaces])

	def iternames(self):
		for name in self.names.values():
			if  self.multiname_names.contains_dst(name):
				multiname = self.multiname_names.get_src(name)
				coll = self.collection_multinames.get_src(multiname)
			else:
				multiname = None
				coll = self.collection_names.get_src(name)
			cl = self.class_names.get_src(name)
			yield (coll, multiname, name, cl)

	def iterstandards(self):
		for std in self.standards.values():
			if  self.multistandard_standards.contains_dst(std):
				multistandard = self.multistandard_standards.get_src(std)
				coll = self.collection_multistandards.get_src(multistandard)
			else:
				multistandard = None
				coll = self.collection_standards.get_src(std)
			cl = self.class_standards.get_src(std)
			yield (coll, multistandard, std, cl)

	def iterclasses(self):
		for cl in self.classes.values():
			coll = self.collection_classes.get_src(cl)
			yield (coll,cl)

	def itercollections(self):
		for coll in self.collections.values():
			yield coll
