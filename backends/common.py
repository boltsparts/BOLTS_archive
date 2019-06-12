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

#common stuff

from os import listdir,makedirs, remove
from os.path import join, exists, isfile
from shutil import rmtree
from .errors import *

UNITS = {"Length (mm)" : "mm", "Length (in)" : "in"}

class Backend:
	"""
	Base class for backends.

	takes care of validating and storing databases, clearing the output directory
	"""
	def __init__(self,repo,name,databases,required=[],optional={}):
		"""
		required and optional are list of strings for databases that
		are required or optional for the correct function of this
		backend
		"""
		self.repo = repo
		self.name = name
		self.dbs = {}
		for db in required:
			if db not in databases:
				raise DatabaseNotAvailableError(self.name,db)
			self.dbs[db] = databases[db]
		for db in optional:
			if db in databases:
				self.dbs[db] = databases[db]
	def clear_output_dir(self,out_dir):
		# pylint: disable=R0201
		if not exists(out_dir):
			makedirs(out_dir)
		for path in listdir(out_dir):
			full_path = join(out_dir,path)
			if isfile(full_path):
				remove(full_path)
			else:
				rmtree(full_path)

	def validate_arguments(self,kwargs,required=[],optional={}):
		"""
		normalises and validates key-value arguments
		kwargs is a dictionary
		required is a list of keys that must be present
		optional is a dict of optional keys, with their default value
		args in kwargs that are not either required or optional are an error conditions
		"""
		res = {}
		res.update(optional)
		for key in kwargs:
			if key in required:
				res[key] = kwargs[key]
			elif key in optional:
				res[key] = kwargs[key]
			else:
				raise UnknownArgumentError(self.name,key)
		return res

	def write_ouput(self,out_path,**kwargs):
		raise NotImplementedError()
