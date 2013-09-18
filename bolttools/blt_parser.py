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

import yaml
import os
from os.path import splitext, split, exists, join
import re
import copy
import openscad,freecad, html, downloads

_re_angled = re.compile("([^<]*)<([^>]*)")

current_version = 0.2

#this is not super-precise, but allows to do some rough checks
_specification = {
	"root" : (["collection","classes"],[]),
	"collection" : (["author","license","blt-version"],["name","description"]),
	"class" : (["naming","source","id"],["drawing","description","standard","status","replaces","parameters","url","notes"]),
	"naming" : (["template"],["substitute"]),
	"parameters" : ([],["literal","free","tables","types"]),
	"table" : (["index","columns","data"],[])
}

class VersionError(Exception):
	def __init__(self,version):
		self.version = version
	def __str__(self):
		return "Unknown version. File: %f Current: %f" % \
			(self.version,current_version)

class UnknownFieldError(Exception):
	def __init__(self,fieldname):
		self.field = fieldname
	def __str__(self):
		return "Unknown Field: %s" % self.field

class MissingFieldError(Exception):
	def __init__(self,fieldname):
		self.field = fieldname
	def __str__(self):
		return "Missing Field: %s" % self.field

class MalformedRepositoryError(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str(self):
		return self.msg

class MalformedCollectionError(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str(self):
		return self.msg

def check_dict(array,spec):
	man = spec[0][:]
	opt = spec[1][:]
	for key in array.keys():
		if key in man:
			man.remove(key)
		elif key in opt:
			opt.remove(key)
		else:
			raise UnknownFieldError(key)
	if len(man) > 0:
		raise MissingFieldError(man)


class BOLTSRepository:
	#order is important
	standard_bodies = ["DINENISO","DINEN","DINISO","DIN","EN","ISO"]
	def __init__(self,path):
		self.path = path
		self.collections = []

		#load collection data
		for filename in os.listdir(join(path,"data")):
			if splitext(filename)[1] == ".blt":
				self.collections.append(BOLTSCollection(join(path,"data",filename)))

		self.standardized = {body:[] for body in self.standard_bodies}

		#find standard parts and their respective standard bodies
		for coll in self.collections:
			for cl in coll.classes:
				#order is important
				for body in self.standard_bodies:
					if cl.name.startswith(body):
						self.standardized[body].append(cl)
						cl.body = body
						break

		#fill in obsolescence data
		for coll in self.collections:
			for cl in coll.classes:
				if cl.replaces is None:
					continue
				#order is important
				for body in self.standard_bodies:
					if cl.replaces.startswith(body):
						idx = [c.name for c in self.standardized[body]].index(cl.replaces)
						self.standardized[body][idx].replacedby = cl.name
						break


		if not exists(join(path,"drawings")):
			raise MalformedRepositoryError("drawings folder is missing")

		#load backend data
		self.openscad = None
		if exists(join(path,"openscad")):
			self.openscad = openscad.OpenSCADData(path)
		self.freecad = None
		if exists(join(path,"freecad")):
			self.freecad = freecad.FreeCADData(path)
		self.html = None
		if exists(join(path,"html")):
			self.html = html.HTMLData(path)
		self.downloads = None
		if exists(join(path,"downloads")):
			self.downloads = downloads.DownloadsData(path)

class BOLTSCollection:
	def __init__(self,bltname):
		self.id = splitext(split(bltname)[1])[0]
		if self.id in ["common","output","data"]:
			raise MalformedCollectionError(
					"Forbidden collection id: %s" % self.id)
		coll = list(yaml.load_all(open(bltname)))
		if len(coll) == 0:
			raise MalformedCollectionError(
					"No YAML document found in file %s" % bltname)
		if len(coll) > 1:
			raise MalformedCollectionError(
					"More than one YAML document found in file %s" % bltname)
		coll = coll[0]

		version = coll["collection"]["blt-version"]
		if version != current_version:
			raise VersionError(version)

		#Check Conformity
		spec = _specification
		try:
			check_dict(coll,spec["root"])
		except (UnknownFieldError, MissingFieldError):
			print "In file %s, field %s" % (bltname,"root")
			raise
		try:
			check_dict(coll["collection"],spec["collection"])
		except (UnknownFieldError, MissingFieldError):
			print "In file %s, field %s" % (bltname,"collection")
			raise
		try:
			check_dict(coll["collection"],spec["collection"])
		except (UnknownFieldError, MissingFieldError):
			print "In file %s, field %s" % (bltname,"collection")
			raise
		classes = coll["classes"]
		if not isinstance(classes,list):
			raise MalformedCollectionError("No class in collection %s"% bltname)
		for cl in classes:
			try:
				check_dict(cl,spec["class"])
			except UnknownFieldError as e:
				raise UnknownFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))
			except MissingFieldError as e:
				raise MissingFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))

			try:
				check_dict(cl["naming"],spec["naming"])
			except UnknownFieldError as e:
				raise UnknownFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))
			except MissingFieldError as e:
				raise MissingFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))

			if "parameters" in cl.keys():
				try:
					check_dict(cl["parameters"],spec["parameters"])
				except UnknownFieldError as e:
					raise UnknownFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))
				except MissingFieldError as e:
					raise MissingFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))
				tables = cl["parameters"]["tables"]
				if isinstance(tables,dict):
					tables = [tables]
				for table,j in zip(tables,range(len(tables))):
					try:
						check_dict(table,spec["table"])
					except UnknownFieldError as e:
						raise UnknownFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))
					except MissingFieldError as e:
						raise MissingFieldError("In file %s, class %s, field %s" % (bltname,cl["id"], e.field))

		#parse header
		header = coll["collection"]
		self.name = ""
		if "name" in header:
			self.name = header["name"]

		self.description = ""
		if "description" in header:
			self.description = header["description"]

		self.authors = header["author"]
		if isinstance(self.authors,str):
			self.authors = [self.authors]

		self.author_names = []
		self.author_mails = []
		for author in self.authors:
			match = _re_angled.match(author)
			self.author_names.append(match.group(1).strip())
			self.author_mails.append(match.group(2).strip())

		self.license = header["license"]
		match = _re_angled.match(self.license)
		self.license_name = match.group(1).strip()
		self.license_url = match.group(2).strip()

		#standardization organisations

		#parse classes
		self.classes = []
		for cl in coll["classes"]:
			names = cl["id"]
			if "standard" in cl:
				names = cl["standard"]
			if isinstance(names,str):
				names = [names]
			for name in names:
				self.classes.append(BOLTSClass(cl,name))

#In contrast to the class-element specified in the blt, this structure has only
#one name, a blt class element gets split into several BOLTSClasses during
#parsing
class BOLTSClass:
	def __init__(self,cl,name):
		self.id = cl["id"]
		self.naming = BOLTSNaming(cl["naming"])

		self.drawing = None
		if "drawing" in cl:
			self.drawing = cl["drawing"]

		self.description = ""
		if "description" in cl:
			self.description = cl["description"]

		self.standard_body = None
		self.standard = None
		self.body = None
		self.status = "active"
		self.replaces = None
		if "standard" in cl:
			self.standard = cl["standard"]
			if isinstance(self.standard,str):
				self.standard = [self.standard]
			if "status" in cl:
				self.status = cl["status"]
				if not self.status in ["active","withdrawn"]:
					raise ValueError
			if "replaces" in cl:
				self.replaces = cl["replaces"]
		#gets updated later by the repo
		self.replacedby = None

		if "parameters" in cl:
			self.parameters = BOLTSParameters(cl["parameters"])
		else:
			self.parameters = BOLTSParameters({})

		self.url = ""
		if "url" in cl:
			self.url = cl["url"]

		self.notes = ""
		if "notes" in cl:
			self.notes = cl["notes"]

		self.source = cl["source"]

		self.name = name

class BOLTSParameters:
	def __init__(self,param):
		self.literal = {}
		if "literal" in param:
			self.literal = param["literal"]

		self.free = []
		if "free" in param:
			self.free = param["free"]

		self.tables = []
		if "tables" in param:
			if isinstance(param["tables"],list):
				for t in param["tables"]:
					self.tables.append(BOLTSTable(t))
			else:
				self.tables.append(BOLTSTable(param["tables"]))

		self.types = {}
		if "types" in param:
			self.types = param["types"]

		self.parameters = []
		self.parameters += self.literal.keys()
		self.parameters += self.free
		for t in self.tables:
			self.parameters.append(t.index)
			self.parameters += t.columns
		#remove duplicates
		self.parameters = list(set(self.parameters))

		#check types
		all_types = ["Length (mm)", "Length (in)", "Number",
			"Bool", "Table Index", "String"]
		
		for k,t in self.types.iteritems():
			if not k in self.parameters:
				raise ValueError("Unknown parameter in types: %s" % k)
			if not t in all_types:
				raise ValueError("Unknown type in types: %s" % t)

		#fill in defaults for types
		for p in self.parameters:
			if not p in self.types:
				self.types[p] = "Length (mm)"

		#check and normalize tables
		for t in self.tables:
			t._normalize_and_check_types(self.types)
	def collect(self,free):
		res = {}
		res.update(self.literal)
		res.update(free)
		for table in self.tables:
			res.update(dict(zip(table.columns,table.data[res[table.index]])))
		for p in self.parameters:
			if not p in res:
				raise KeyError("Parameter value not collected: %s" % p)
		return res

class BOLTSTable:
	def __init__(self,table):
		self.index = table["index"]
		self.columns = table["columns"]
		self.data = copy.deepcopy(table["data"])

	def _normalize_and_check_types(self,types):
		numbers = ["Length (mm)", "Length (in)", "Number"]
		positive = ["Length (mm)", "Length (in)"]
		rest = ["Bool", "Table Index", "String"]
		col_types = [types[col] for col in self.columns]
		idx = range(len(self.columns))
		for key in self.data:
			row = self.data[key]
			for i,t in zip(idx,col_types):
				if row[i] == "None":
					row[i] = None
				else:
					if t in numbers:
						row[i] = float(row[i])
					elif not t in rest:
						raise ValueError("Unknown Type in table: %s" % t)
					if t in positive and row[i] < 0:
						raise ValueError("Negative length in table: %f" % row[i])
					if t == "Bool":
						row[i] = bool(row[i])

class BOLTSNaming:
	def __init__(self,name):
		self.template = name["template"]
		self.substitute = []
		if "substitute" in name:
			self.substitute = name["substitute"]
	def get_name(self,params):
		return self.template % (params[s] for s in self.substitute)
