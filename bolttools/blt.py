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
import os
from os.path import splitext, exists, join
# pylint: disable=W0622
from codecs import open

from errors import *
from common import Parameters, Identifier, Substitution, parse_angled, check_schema

CURRENT_VERSION = 0.4

class DesignationMixin:
	"""
	Mixin for classes that allow to refer to a class.
	"""
	def __init__(self):
		pass
	def get_id(self):
		raise NotImplementedError

class ClassName(DesignationMixin):
	"""
	Python class to provide a name for a BOLTS class, corresponding to a
	ClassNameElement in the blt file.
	"""
	def __init__(self,cn,clid):
		check_schema(cn,"classname",
			["name","labeling"],
			["description","group"]
		)
		DesignationMixin.__init__(self)

		try:
			self.name = Identifier(cn['name'])
			self.labeling = Substitution(cn['labeling'])
		except ParsingError as e:
			e.set_class(self.id)
			raise e

		self.description = ''
		if 'description' in cn:
			self.description = cn['description']

		try:
			if 'group' in cn:
				self.group = Identifier(cn['group'])
			else:
				self.group = Identifier({'nice' : ""})
		except ParsingError as e:
			e.set_class(clid)
			raise e

		self.classid = clid
	def get_id(self):
		if self.group.get_safe_name():
			return self.group.get_safe_name() + "_" + self.name.get_safe_name()
		else:
			return self.name.get_safe_name()


class StandardName(DesignationMixin):
	"""
	Python class to provide a standard name for a BOLTS class, corresponding to a
	ClassStandardElement in the blt file.
	"""
	def __init__(self,sn,clid):
		check_schema(sn,'classstandard',
			['standard','labeling','body'],
			['suffix','year','status','replaces','description']
		)
		DesignationMixin.__init__(self)

		try:
			self.standard = Identifier(sn['standard'])
			if 'suffix' in sn:
				self.suffix = Identifier(sn['suffix'])
			else:
				self.suffix = Identifier({'nice' : ""})
			self.labeling = Substitution(sn['labeling'])
		except ParsingError as e:
			e.set_class(clid)
			raise e

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

		self.classid = clid
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

class ContainerMixin:
	"""A mixin that provides the infrastrucutre to contain a number of BOLTS classes"""
	def __init__(self,allowed=['name_single','name_group','standard_single','standard_multi']):
		self.allowed = allowed

		self.names_single = {}
		self.names_group = {}
		self.standards_single = {}
		self.standards_multi = {}
		self.everything = {}

	def add_name_single(self,cn):
		if not 'name_single' in self.allowed:
			raise ValueError("This container is not allowed to hold names")
		if cn.get_id() in self.everything:
			raise MalformedRepositoryError("Duplicate name %s" % cn.get_id())
		self.names_single[cn.get_id()] = cn
		self.everything[cn.get_id()] = cn

	def contains_name_single(self,id):
		return id in self.names_single
	
	def get_name_single(self,id):
		return self.names_single[id]

	def all_names_single(self):
		for name in self.names_single.values():
			yield name

	def add_name_group(self,cng):
		if not 'name_group' in self.allowed:
			raise ValueError("This container is not allowed to hold name groups")
		if cng.get_id() in self.everything:
			raise MalformedRepositoryError("Duplicate name %s" % cng.get_id())

		for cn in cng.all_names_single():
			if cn.get_id() in self.everything:
				raise MalformedRepositoryError("Duplicate name %s" % cn.get_id())
		self.names_group[cng.get_id()] = cng
		self.everything[cng.get_id()] = cng
		for cn in cng.all_names_single():
			self.everything[cn.get_id()] = cn

	def contains_name_group(self,id):
		return id in self.names_group

	def get_name_group(self,id):
		return self.names_group[id]

	def all_names_group(self):
		for ng in self.names_group.values():
			yield ng

	def add_standard_single(self,cs):
		if not 'standard_single' in self.allowed:
			raise ValueError("This container is not allowed to hold single standards")
		if cs.get_id() in self.everything:
			raise MalformedRepositoryError("Duplicate standard %s" % cs.get_id())

		self.standards_single[cs.get_id()] = cs
		self.everything[cs.get_id()] = cs

	def contains_standard_single(self,id):
		return id in self.standards_single

	def get_standard_single(self,id):
		return self.standards_single[id]

	def all_standards_single(self):
		for standard in self.standards_single.values():
			yield standard

	def add_standard_multi(self,cs):
		if not 'standard_multi' in self.allowed:
			raise ValueError("This container is not allowed to hold multi standards")
		if cs.get_id() in self.everything:
			raise MalformedRepositoryError("Duplicate standard %s" % cs.get_id())
		for st in cs.all_standards_single():
			if st.get_id() in self.everything:
				raise MalformedRepositoryError("Duplicate standard %s" % st.get_id())

		self.standards_multi[cs.get_id()] = cs
		self.everything[cs.get_id()] = cs
		for st in cs.all_standards_single():
			self.everything[st.get_id()] = st

	def contains_standard_multi(self,id):
		return id in self.standards_multi

	def get_standard_multi(self,id):
		return self.standards_multi[id]

	def all_standards_multi(self):
		for standard in self.standards_multi.values():
			yield standard

	def contains_standard(self,id):
		if id in self.standards_single:
			return True
		else:
			for ms in self.standards_multi.values():
				if ms.contains_standard_single(id):
					return True
		return False

	def get_standard(self,id):
		"""returns single standards"""
		if id in self.standards_single:
			return self.standards_single[id]
		else:
			for ms in self.standards_multi.values():
				if ms.contains_standard_single(id):
					return ms.get_standard_single(id)
		raise KeyError('id: %s not known' % id)

	def all_standards(self):
		"""returns single standards"""
		for standard in self.standards_single.values():
			yield standard
		for ms in self.standards_multi.values():
			for standard in ms.all_standards_single():
				yield standard

	def contains_name(self,id):
		if id in self.names_single:
			return True
		else:
			for ng in self.names_group.values():
				if ng.contains_name_single(id):
					return True
		return False

	def get_name(self,id):
		""" returns single names, no name groups"""
		if id in self.names_single:
			return self.names_single[id]
		else:
			for ng in self.names_group.values():
				if ng.contains_name_single(id):
					return ms.get_name_single(id)
		raise KeyError('id: %s not known' % id)

	def all_names(self):
		""" returns single names, no name groups"""
		for name in self.names_single.values():
			yield name
		for ng in self.names_group.values():
			for name in ng.all_names_single():
				yield name

	def contains(self,id):
		return id in self.everything
	
	def get(self,id):
		"""might return any designation"""
		return self.everything[id]




class Collection(ContainerMixin):
	"""
	Container for all classes contained in a BOLTS Collection
	"""
	def __init__(self,coll):
		check_schema(coll,"collection",
			["id","author","license","blt-version","classes"],
			["name","description"]
		)
		ContainerMixin.__init__(self)

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

class StandardBody(ContainerMixin):
	"""
	Container for standard names that are specified by a common
	standardisation body
	"""
	def __init__(self,body):
		self.body = body
		ContainerMixin.__init__(self,['standard_single','standard_multi'])

class MultipartStandard(ContainerMixin,DesignationMixin):
	"""
	Container for all standard names that are covered by a single standard
	"""
	def __init__(self,standard):
		ContainerMixin.__init__(self,['standard_single'])
		DesignationMixin.__init__(self)

		self.standard = standard

	def get_id(self):
		return self.standard.get_safe_name()

	def add_standard_single(self,cs):
		if cs.standard != self.standard:
			raise RuntimeError("Multipart standard with conflicting standards: %s %s" %
				(cs.standard.get_safe_name(), self.standard.get_safe_name()))
		ContainerMixin.add_standard_single(self,cs)

class NameGroup(ContainerMixin,DesignationMixin):
	"""
	Container for all class names that are part of a common group
	"""
	def __init__(self,group):
		ContainerMixin.__init__(self,['name_single'])
		DesignationMixin.__init__(self)

		self.group = group
	def get_id(self,cn):
		return self.group.get_safe_name()

	def add_name_single(self,cn):
		if self.group != cn.group:
			raise RunrimeError("Name group with conflicting group names: %s %s" %
				(cn.group.get_safe_name(), self.group.get_safe_name()))

class Repository(ContainerMixin):
	def __init__(self,path):
		ContainerMixin.__init__(self)

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

		self.classes = {}

		self.collections = {}

		self.standard_bodies = {}

		self.name_groups = {}

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
					name = ClassName(cn,cl['id'])

					groupname = name.group.get_safe_name()

					if groupname:
						for cont in [self,coll]:
							group = None
							if groupname in cont.name_groups:
								group = cont.get_name_group(groupname)
							else:
								group = NameGroup(name.group)
								cont.add_name_group(group)
							group.add_name_single(name)
					else:
						for cont in [self,coll]:
							cont.add_name_single(name)

				for sn in standards:
					standard = StandardName(sn,cl['id'])

					body = None
					if standard.body in self.standard_bodies:
						body = self.standard_bodies[standard.body]
					else:
						body = StandardBody(standard.body)
						self.standard_bodies[standard.body] = body

					if standard.suffix.get_safe_name():
						for cont in [self,coll,body]:
							mult = None
							if cont.contains_standard_multi(standard.standard):
								mult = cont.get_standard_multi(standard.standard)
							else:
								mult = MultipartStandard(standard.standard)
								cont.add_standard_multi(mult)
							mult.add_standard_single(standard)
					else:
						for cont in [self,coll,body]:
							cont.add_standard_single(standard)


		#fill in obsolescence data
		for standard in self.all_standards():
			if standard.replaces is None:
				continue
			if not self.contains_standard(standard.replaces):
				raise MalformedRepositoryError(
					"Unknown replace field in standard %s" % standard.get_id())
			standard.replacedby = standard.replaces
