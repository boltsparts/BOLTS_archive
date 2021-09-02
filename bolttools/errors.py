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

class ParsingError(Exception):
    def __init__(self):
        Exception.__init__(self)
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
        trace = " ".join("%s: %s" % (k,str(v))
            for k,v in self.trace_info.items())
        return "%s.  %s" % (self.msg, trace)

class VersionError(ParsingError):
    def __init__(self,version):
        ParsingError.__init__(self)
        self.msg = "Old or unknown version: %g" % version

class UnknownFieldError(ParsingError):
    def __init__(self,elementname,fieldname):
        ParsingError.__init__(self)
        self.msg = "Unknown field %s in %s" % (fieldname,elementname)

class MissingFieldError(ParsingError):
    def __init__(self,elementname, fieldname):
        ParsingError.__init__(self)
        self.msg = "Missing mandatory field %s in %s" % (fieldname,elementname)

class MalformedRepositoryError(ParsingError):
    def __init__(self,msg):
        ParsingError.__init__(self)
        self.msg = msg

class MalformedCollectionError(ParsingError):
    def __init__(self,msg):
        ParsingError.__init__(self)
        self.msg = msg

class MalformedBaseError(ParsingError):
    def __init__(self,msg):
        ParsingError.__init__(self)
        self.msg = msg

class MalformedStringError(ParsingError):
    def __init__(self,msg):
        ParsingError.__init__(self)
        self.msg = msg

class NonFreeDefaultError(ParsingError):
    def __init__(self,pname):
        ParsingError.__init__(self)
        self.msg = "Default value given for non-free parameter %s" % pname

class UnknownParameterError(ParsingError):
    def __init__(self,pname):
        ParsingError.__init__(self)
        self.msg = "Unknown parameter in types: %s" % pname

class UnknownTypeError(ParsingError):
    def __init__(self,tname):
        ParsingError.__init__(self)
        self.msg = "Unknown type in types: %s" % tname

class MissingTypeError(ParsingError):
    def __init__(self,pname):
        ParsingError.__init__(self)
        self.msg = "No type specified for parameter: %s" % pname

class NonUniqueBaseError(ParsingError):
    def __init__(self,id):
        ParsingError.__init__(self)
        self.msg = "Encountered more than one base for class with id: %s" % id

class NonUniqueClassIdError(ParsingError):
    def __init__(self,id):
        ParsingError.__init__(self)
        self.msg = "Encountered more than one class with id: %s" % id

class MalformedTableIndexError(ParsingError):
    def __init__(self,val):
        ParsingError.__init__(self)
        self.msg = "%s is not a valid Table Index" % (val)

class InvalidTableIndexError(ParsingError):
    def __init__(self,pname,val):
        ParsingError.__init__(self)
        self.msg = "%s is not a valid choice as a Table Index for parameter %s" % (val,pname)

class MissingLocationError(ParsingError):
    def __init__(self,arguments):
        ParsingError.__init__(self)
        self.msg = "Argument list for coordinate system does not contain 'location': %s" % arguments

class TableIndexTypeError(ParsingError):
    def __init__(self,pname,tname):
        ParsingError.__init__(self)
        self.msg = "Parameter %s is used as an index in a table but has type: %s" % (pname,tname)

class IncompatibleTypeError(Exception):
    def __init__(self,pname,tname1,tname2):
        Exception.__init__(self)
        self.msg = "Type conflict on Parameter union for %s: %s is not %s" % (pname,tname1,tname2)
    def __str__(self):
        return self.msg

class IncompatibleDefaultError(Exception):
    def __init__(self,pname,dname1,dname2):
        Exception.__init__(self)
        self.msg = "Default value conflict on Parameter union for %s: %s is not %s" % (pname,dname1,dname2)
    def __str__(self):
        return self.msg

class IncompatibleDescriptionError(Exception):
    def __init__(self,pname,d1,d2):
        Exception.__init__(self)
        self.msg = "Description conflict on Parameter union for %s: %s is not %s" % (pname,d1,d2)
    def __str__(self):
        return self.msg

class LimitExceededError(Exception):
    def __init__(self,src,dst):
        self.msg = "Destination limit exceeded when trying to insert link %s,%s" % (src,dst)
    def __str__(self):
        return self.msg
