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

class BackendError(Exception):
	def __init__(self,backendname):
		Exception.__init__(self)
		self.backendname = backendname
		self.msg = ""
	def __str__(self):
		return "Problem in backend %s:\n" + self.msg

class UncommitedChangesError(Exception):
	def __str__(self):
		return "There are uncommitted changes in the git repo"

class NonUniqueClassIdError(Exception):
	def __init__(self,id):
		Exception.__init__(self)
		self.cl_id = id
	def __str__(self):
		return "Encountered more than one class with the same id: %s" % self.cl_id

class IncompatibleLicenseError(Exception):
	def __init__(self,msg):
		Exception.__init__(self)
		self.msg = msg
	def __str__(self):
		return self.msg

class DatabaseNotAvailableError(BackendError):
	def __init__(self,backendname,db):
		BackendError.__init__(self,"")
		self.msg = "The database %s is required by this backend, but was not passed" % db

class MissingArgumentError(BackendError):
	def __init__(self,backendname,kw):
		BackendError.__init__(self,"")
		self.msg = "The required keyword argument %s was not supplied" % kw

class UnknownArgumentError(BackendError):
	def __init__(self,backendname,kw):
		BackendError.__init__(self,"")
		self.msg = "An unknown keyword argument %s was supplied" % kw

class ModuleNameCollisionError(Exception):
	def __init__(self,modulename):
		Exception.__init__(self)
		self.modulename = modulename
	def __str__(self):
		return "Detected a module name clash for OpenSCAD export for name: %s" % self.modulename

class MissingFreeCADError(Exception):
	def __init__(self):
		Exception.__init__(self)
	def __str__(self):
		return "Could not find FreeCAD python module"

class FileNotFoundError(Exception):
	def __init__(self,filename):
		Exception.__init__(self)
		self.filename = filename
	def __str__(self):
		return "Could not find file %s. BOLTS is case sensitive" % self.filename
