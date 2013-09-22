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

class ParsingError(Exception):
	def __init__(self):
		self.trace_info = {}
		self.msg = "Something went wrong with parsing"
	def set_repo_path(self,path):
		self.trace_info["Repository path"] = path
	def set_collection(self,coll):
		self.trace_info["Collection"] = coll
	def set_class(self,cl):
		self.trace_info["Class"] = cl
	def set_base(self,base):
		self.trace_info["Base"] = base
	def __str__(self):
		trace = " ".join("%s: %s" % (k,str(v)) for k,v in self.trace_info.iteritems())
		return "%s.  %s" % (self.msg, trace)

class VersionError(ParsingError):
	def __init__(self,version):
		ParsingError.__init__(self)
		self.msg = "Old or unknown version: %g" % version

class UnknownFieldError(ParsingError):
	def __init__(self,fieldname):
		ParsingError.__init__(self)
		self.msg = "Unknown Field: %s" % fieldname

class MissingFieldError(ParsingError):
	def __init__(self,fieldname):
		ParsingError.__init__(self)
		self.msg = "Missing Field: %s" % fieldname

class MalformedRepositoryError(ParsingError):
	def __init__(self,msg):
		ParsingError.__init__(self)
		self.msg = msg

class MalformedCollectionError(ParsingError):
	def __init__(self,msg):
		ParsingError.__init__(self)
		self.msg = msg

