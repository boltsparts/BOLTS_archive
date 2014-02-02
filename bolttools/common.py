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

#common elements and baseclasses

import re
import math
from os.path import join
from copy import deepcopy

from errors import *

RE_ANGLED = re.compile("([^<]*)<([^>]*)>")

def parse_angled(string):
	match = RE_ANGLED.match(string)
	if match is None:
		raise MalformedStringError("Expected string containing <>")
	return match.group(1).strip(), match.group(2).strip()

def check_schema(yaml_dict, element_name, mandatory_fields, optional_fields):
	#check dict from YAML parsing for correct and complete fields
	for key in yaml_dict.keys():
		if key in mandatory_fields:
			mandatory_fields.remove(key)
		elif key in optional_fields:
			optional_fields.remove(key)
		else:
			raise UnknownFieldError(element_name,key)
	if len(mandatory_fields) > 0:
		raise MissingFieldError(element_name,mandatory_fields)

ALL_TYPES = ["Length (mm)", "Length (in)", "Number", "Bool", "Table Index", "String","Angle (deg)"]

def convert_type(pname,tname,value):
	""" Convert from strings to python types """
	numbers = ["Length (mm)", "Length (in)", "Number","Angle (deg)"]
	positive = ["Length (mm)", "Length (in)"]

	#Check
	if not tname in ALL_TYPES:
		raise ValueError("Unknown Type in table for parameter %s: %s" % (pname,tname))

	#Convert
	if value == "None":
		value = None
	elif tname in numbers:
		value = float(value)
		if tname in positive and value < 0:
			raise ValueError("Negative length in table for parameter %s: %f" % (pname,value))
		elif tname == "Angle (deg)" and math.fabs(value) > 360:
			raise ValueError("Angles must be 360 > alpha > -360: %s is %f" % (pname,value))
	elif tname == "Bool":
		if not value in ["True","False"]:
			raise ValueError("Unknown value for bool parameter %s: %s" % value)
		value = bool(value)

	return value

class Sorting:
	def __init__(self):
		pass
	def is_applicable(self,choices):
		return False
	def sort(self,choices):
		return choices

class Numerical(Sorting):
	def __init__(self):
		Sorting.__init__(self)
		self.re = re.compile("[^0-9]*([0-9]+\.*[0-9]*)[^0-9]*$")
	def is_applicable(self,choices):
		for choice in choices:
			if self.re.match(choice) is None:
				return False
		return True
	def sort(self,choices):
		return sorted(choices, key=lambda x: float(self.re.match(x).group(1)))

class Alphabetical(Sorting):
	def __init__(self):
		Sorting.__init__(self)
	def is_applicable(self,choices):
		return True
	def sort(self,choices):
		return sorted(choices)

SORTINGS = [Numerical(), Alphabetical()]

class BOLTSParameters:
	type_defaults = {
		"Length (mm)" : 10,
		"Length (in)" : 1,
		"Number" : 1,
		"Bool" : False,
		"Table Index": '',
		"String" : '',
		"Angle (deg)" : 0
	}
	def __init__(self,param):
		check_schema(param,"parameters",
			["types"],
			["literal","free","tables","tables2d","defaults","common","description"]
		)

		self.types = {}
		if "types" in param:
			self.types = param["types"]

		self.literal = {}
		if "literal" in param:
			for pname,val in param["literal"].iteritems():
				self.literal[pname] = convert_type(pname,self.types[pname],val)

		self.free = []
		if "free" in param:
			self.free = param["free"]

		self.tables = []
		if "tables" in param:
			if isinstance(param["tables"],list):
				for table in param["tables"]:
					self.tables.append(BOLTSTable(table))
			else:
				self.tables.append(BOLTSTable(param["tables"]))

		self.tables2d = []
		if "tables2d" in param:
			if isinstance(param["tables2d"],list):
				for table in param["tables2d"]:
					self.tables2d.append(BOLTSTable2D(table))
			else:
				self.tables2d.append(BOLTSTable2D(param["tables2d"]))

		self.description = {}
		if "description" in param:
			self.description = param["description"]

		self.parameters = []
		self.parameters += self.literal.keys()
		self.parameters += self.free
		for table in self.tables:
			self.parameters.append(table.index)
			self.parameters += table.columns
		for table in self.tables2d:
			self.parameters.append(table.rowindex)
			self.parameters.append(table.colindex)
			self.parameters.append(table.result)
		#remove duplicates
		self.parameters = list(set(self.parameters))

		#check types
		for pname,tname in self.types.iteritems():
			if not pname in self.parameters:
				raise UnknownParameterError(pname)
			if not tname in ALL_TYPES:
				raise UnknownTypeError(tname)

		for pname in self.parameters:
			if not pname in self.types:
				raise MissingTypeError(pname)

		#check description
		for pname,tname in self.description.iteritems():
			if not pname in self.parameters:
				raise UnknownParameterError(pname)

		#check and normalize tables
		for table in self.tables:
			table._normalize_and_check_types(self.types)
			if self.types[table.index] != "Table Index":
				raise TableIndexTypeError(table.index,self.types[table.index])
		for table in self.tables2d:
			table._normalize_and_check_types(self.types)
			if self.types[table.rowindex] != "Table Index":
				raise TableIndexTypeError(table.rowindex,self.types[table.rowindex])
			if self.types[table.colindex] != "Table Index":
				raise TableIndexTypeError(table.colindex,self.types[table.colindex])

		#find the set of possible choices for every Table Index
		self.choices = {}
		for pname in self.free:
			if not self.types[pname] == "Table Index":
				continue
			for table in self.tables:
				if table.index == pname:
					if not pname in self.choices:
						self.choices[pname] = set(table.data.keys())
					else:
						self.choices[pname] &= set(table.data.keys())
			for table in self.tables2d:
				if table.rowindex == pname:
					if not pname in self.choices:
						self.choices[pname] = set(table.data.keys())
					else:
						self.choices[pname] &= set(table.data.keys())
				elif table.colindex == pname:
					if not pname in self.choices:
						self.choices[pname] = set(table.columns)
					else:
						self.choices[pname] &= set(table.columns)
		#figure out what the best way is to sort them
		for pname in self.choices:
			for sort in SORTINGS:
				if sort.is_applicable(self.choices[pname]):
					self.choices[pname] = sort.sort(self.choices[pname])
					break

		#default values for free parameters
		self.defaults = dict((pname,self.type_defaults[self.types[pname]])
			for pname in self.free)
		if "defaults" in param:
			for pname,dvalue in param["defaults"].iteritems():
				if pname not in self.free:
					raise NonFreeDefaultError(pname)
				if self.types[pname] == "Table Index" and dvalue not in self.choices[pname]:
					raise InvalidTableIndexError(pname,dvalue)
				self.defaults[pname] = dvalue

		#common parameter combinations
		discrete_types = ["Bool", "Table Index"]
		self.common = None
		if "common" in param:
			self.common = []
			for tup in param["common"]:
				self._populate_common(tup,[],0)
		else:
			discrete = True
			for pname in self.free:
				if not self.types[pname] in discrete_types:
					discrete = False
					break
			if discrete:
				self.common = []
				if len(self.free) > 0:
					self._populate_common([":" for _i in range(len(self.free))],[],0)
				else:
					self.common.append([])

	def _populate_common(self, tup, values, idx):
		if idx == len(self.free):
			self.common.append(values)
		else:
			if tup[idx] == ":":
				if self.types[self.free[idx]] == "Bool":
					for v in [True, False]:
						self._populate_common(tup,values + [v], idx+1)
				elif self.types[self.free[idx]] == "Table Index":
					#populate
					for v in self.choices[self.free[idx]]:
						self._populate_common(tup,values + [v], idx+1)
				else:
					print "That should not happen"
			else:
				for v in tup[idx]:
					self._populate_common(tup,values + [v], idx+1)

	def collect(self,free):
		res = {}
		res.update(self.literal)
		res.update(free)
		for table in self.tables:
			res.update(dict(zip(table.columns,table.data[res[table.index]])))
		for table in self.tables2d:
			row = table.data[res[table.rowindex]]
			res[table.result] = row[table.columns.index(res[table.colindex])]
		for pname in self.parameters:
			if not pname in res:
				raise KeyError("Parameter value not collected: %s" % pname)
		return res

	def union(self,other):
		res = BOLTSParameters({"types" : {}})
		res.literal.update(self.literal)
		res.literal.update(other.literal)
		res.free = self.free + other.free
		res.tables = self.tables + other.tables
		res.tables2d = self.tables2d + other.tables2d
		res.parameters = list(set(self.parameters))

		for pname,tname in self.types.iteritems():
			res.types[pname] = tname
		for pname,tname in other.types.iteritems():
			if pname in res.types and self.types[pname] != tname:
				raise IncompatibleTypeError(pname,self.types[pname],tname)
			res.types[pname] = tname

		for pname,dname in self.defaults.iteritems():
			res.defaults[pname] = dname
		for pname,dname in other.defaults.iteritems():
			if pname in res.defaults and self.defaults[pname] != dname:
				raise IncompatibleDefaultError(pname,self.defaults[pname],dname)
			res.defaults[pname] = dname

		for pname,descr in self.description.iteritems():
			res.description[pname] = descr
		for pname,descr in other.description.iteritems():
			if pname in res.description and self.description[pname] != descr:
				raise IncompatibleDescriptionError(pname,self.description[pname],descr)
			res.description[pname] = descr

		res.choices = {}
		for pname in self.choices:
			res.choices[pname] = set(self.choices[pname])
		for pname in other.choices:
			if pname in res.choices:
				res.choices[pname] &= set(other.choices[pname])
			else:
				res.choices[pname] = set(other.choices[pname])
		sortings = [Numerical(), Alphabetical()]
		for pname in res.choices:
			for sort in SORTINGS:
				if sort.is_applicable(res.choices[pname]):
					res.choices[pname] = sort.sort(res.choices[pname])
					break
		return res

class BOLTSTable:
	def __init__(self,table):
		check_schema(table,"table",
			["index","columns","data"],
			[]
		)

		self.index = table["index"]
		self.columns = table["columns"]
		self.data = deepcopy(table["data"])

	def _normalize_and_check_types(self,types):
		col_types = [types[col] for col in self.columns]
		for key in self.data:
			row = self.data[key]
			if len(row) != len(self.columns):
				raise ValueError("Column is missing for row: %s" % key)
			for i in range(len(self.columns)):
				row[i] = convert_type(self.columns[i],col_types[i],row[i])

class BOLTSTable2D:
	def __init__(self,table):
		check_schema(table,"table2d",
			["rowindex","colindex","columns","result","data"],
			[]
		)

		self.rowindex = table["rowindex"]
		self.colindex = table["colindex"]
		self.result = table["result"]
		self.columns = table["columns"]
		self.data = deepcopy(table["data"])

		if self.rowindex == self.colindex:
			raise ValueError("Row- and ColIndex are identical. In this case a ordinary table should be used.")

	def _normalize_and_check_types(self,types):
		res_type = types[self.result]
		for key in self.data:
			row = self.data[key]
			if len(row) != len(self.columns):
				raise ValueError("Column is missing for row: %s" % key)
			for i in range(len(self.columns)):
				row[i] = convert_type(self.result,types[self.result],row[i])

class BOLTSNaming:
	def __init__(self,name):
		check_schema(name,"naming",
			["template"],
			["substitute"]
		)

		self.template = name["template"]
		self.substitute = []
		if "substitute" in name:
			self.substitute = name["substitute"]

	def get_name(self,params):
		return self.template % tuple(params[s] for s in self.substitute)


class DataBase:
	def __init__(self,name,path):
		self.repo_root = path
		self.backend_root = join(path,name)

class BaseElement:
	def __init__(self,basefile,collname):
		self.collection = collname

		self.authors = basefile["author"]
		if isinstance(self.authors,str):
			self.authors = [self.authors]
		self.author_names = []
		self.author_mails = []
		for author in self.authors:
			match = parse_angled(author)
			self.author_names.append(match[0])
			self.author_mails.append(match[1])

		self.license = basefile["license"]
		match = parse_angled(self.license)
		self.license_name = match[0]
		self.license_url = match[1]

		self.type = basefile["type"]

		self.source = ""
		if "source" in basefile:
			self.source = basefile["source"]
