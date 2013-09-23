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

from errors import *
from common import BackendData, BackendExporter
from os import listdir,makedirs
from os.path import join, exists, basename
from shutil import rmtree,copy
import yaml

_openscad_base_specification = {
	"file-module" : (["filename","author","license","type","modules"],[]),
	"file-stl" : (["filename","author","license","type","classids"],["baseid"]),
	"module" : (["name", "arguments","classids"],["baseid"]),
}

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

class OpenSCADBase:
	def __init__(self,basefile,collname):
		self.collection = collname
		self.filename = basefile["filename"]
		self.path = join(collname,self.filename)
		self.author = basefile["author"]
		self.license = basefile["license"]
	def get_copy_files(self):
		"Returns the path of the files to copy relative to the backend_root"
		raise NotImplementedError
	def get_include_files(self):
		"Returns the path of the files to copy relative to the base folder in output"
		raise NotImplementedError
	def get_incantation(self,args):
		"Return the incantation of the base that produces the geometry"
		raise NotImplementedError

class BaseModule(OpenSCADBase):
	def __init__(self,mod,basefile,collname):
		self._check_conformity(mod,basefile)
		OpenSCADBase.__init__(self,basefile,collname)
		self.baseid = mod["name"]
		if "baseid" in mod:
			self.baseid = mod["baseid"]
		self.name = mod["name"]
		self.arguments = mod["arguments"]
		self.classids = mod["classids"]
	def _check_conformity(self,mod,basefile):
		spec = _openscad_base_specification
		check_dict(mod,spec["module"])
		check_dict(basefile,spec["file-module"])
	def get_copy_files(self):
		return [self.path]
	def get_include_files(self):
		return [self.filename]
	def get_incantation(self,args):
		return "%s(%s)" % (self.name,", ".join(args[arg] for arg in self.arguments))


class BaseSTL(OpenSCADBase):
	def __init__(self,basefile,collname):
		self._check_conformity(basefile)
		OpenSCADBase.__init__(self,basefile,collname)
		self.baseid = self.filename
		if "baseid" in basefile:
			self.baseid = basefile["baseid"]
		self.classids = basefile["classids"]
	def _check_conformity(self,basefile):
		spec = _openscad_base_specification
		check_dict(basefile,spec["file-stl"])
	def get_copy_files(self):
		return [self.path]
	def get_include_files(self):
		return []
	def get_incantation(self,args):
		return 'import("%s")' % join("base",self.filename)


class OpenSCADData(BackendData):
	def __init__(self,path):
		BackendData.__init__(self,"openscad",path)
		#maps class id to base module
		self.getbase = {}

		for coll in listdir(self.backend_root):
			basename = join(self.backend_root,coll,"%s.base" % coll)
			if not exists(basename):
				#skip directory that is no collection
				continue
			base =  list(yaml.load_all(open(basename)))
			if len(base) != 1:
				raise MalformedCollectionError(
						"No YAML document found in file %s" % bltname)
			base = base[0]
			for basefile in base:
				if basefile["type"] == "module":
					for mod in basefile["modules"]:
						try:
							module = BaseModule(mod,basefile,coll)
							for id in module.classids:
								if id in self.getbase:
									raise NonUniqueClassIdentifier
								self.getbase[id] = module
						except ParsingError as e:
							e.set_base(basefile["filename"])
							raise e
				elif basefile["type"] == "stl":
					try:
						module = BaseSTL(basefile,coll)
						for id in module.classids:
							if id in self.getbase:
								raise NonUniqueClassIdentifier
							self.getbase[id] = module
					except ParsingError as e:
						e.set_base(basefile["filename"])
						raise e

class OpenSCADExporter(BackendExporter):
	def write_output(self,repo):
		oscad = repo.openscad
		out_path = oscad.out_root

		self.clear_output_dir(oscad)
		#copy files
		bolts_fid = open(join(out_path,"BOLTS.scad"),"w")
		standard_fids = {}
		for std in repo.standard_bodies:
			standard_fids[std] = open(join(out_path,"BOLTS_%s.scad" % std),"w")

		makedirs(join(out_path,"tables"))

		#copy common files
		makedirs(join(out_path,"common"))
		for filename in listdir(join(oscad.backend_root,"common")):
			copy(join(oscad.backend_root,"common",filename),join(out_path,"common",filename))
			bolts_fid.write("include <common/%s>\n" % filename)
			for std in standard_fids:
				standard_fids[std].write("include <common/%s>\n" % filename)

		#copy base files
		copied = []
		makedirs(join(out_path,"base"))
		for id in oscad.getbase:
			for path in oscad.getbase[id].get_copy_files():
				if path in copied:
					continue
				copy(join(oscad.backend_root,path),join(out_path,"base",basename(path)))
				copied.append(path)

		#include files
		included = []
		for id in oscad.getbase:
			for path in oscad.getbase[id].get_include_files():
				if path in included:
					continue
				bolts_fid.write("include <base/%s>\n" % path)
				for std in standard_fids:
					standard_fids[std].write("include <base/%s>\n" % path)
				included.append(path)

		#write tables
		for collection in repo.collections:
			for cl in collection.classes:
				if not cl.id in repo.openscad.getbase:
					continue
				table_path = join("tables","%s_table.scad" % cl.name)
				table_filename = join(out_path,table_path)
				fid = open(table_filename,"w")
				self.write_table(fid,collection,cl)
				fid.close()

				bolts_fid.write("include <%s>\n" % table_path)
				for std in standard_fids:
					if cl in repo.standardized[std]:
						standard_fids[std].write("include <%s>\n" % table_path)
		bolts_fid.write("\n\n")

		#write stubs
		for collection in repo.collections:
			for cl in collection.classes:
				if not cl.id in repo.openscad.getbase:
					continue
				self.write_stub(repo,bolts_fid,cl)
				for std in standard_fids:
					if cl in repo.standardized[std]:
						self.write_stub(repo,standard_fids[std],cl)
		bolts_fid.close()
		for std in standard_fids:
			standard_fids[std].close()

	def write_table(self,fid,collection,cl):
		for table,i in zip(cl.parameters.tables,range(len(cl.parameters.tables))):
			cols = table.columns
			fid.write("/* Generated by BOLTS, do not modify */\n")
			fid.write("/* Copyright by: %s */\n" % ",".join(collection.authors))
			fid.write("/* %s */\n" % collection.license)

			data = table.data

			fid.write("function %s_table_%d(key) = \n" % (cl.name,i))
			for k,values in data.iteritems():
				data = ["None" if v is None else v for v in values]
				fid.write('key == "%s" ? %s : \n' % (k,str(data).replace("'",'"')))
			fid.write('"Error";\n\n')

	def write_stub(self,repo,fid,cl):
		#collect textual parameter representations
		args = {}
		if not cl.standard is None:
			args['standard'] = '"%s"' % cl.name
		params = cl.parameters
		for p in params.free:
			args[p] = p
		args.update(params.literal)
		for table,i in zip(params.tables,range(len(params.tables))):
			for p,j in zip(table.columns,range(len(table.columns))):
				args[p] = 'measures_%d[%d]' % (i,j)

		arg_strings = []
		for p in params.free:
			if params.types[p] in ["String","Table Index"]:
				arg_strings.append('%s="%s"' % (p,params.defaults[p]))
			else:
				arg_strings.append('%s=%s' % (p,params.defaults[p]))
		fid.write('module %s(%s){\n' % (cl.name, ', '.join(arg_strings)))

		#warnings and type checks
		if cl.status == "withdrawn":
			fid.write('\techo("Warning: The standard %s is withdrawn. Although withdrawn standards are often still in use, it might be better to use its successor %s instead");\n' % (cl.name,cl.replacedby))
		for p in params.free:
			fid.write('\tcheck_parameter_type("%s","%s",%s,"%s");\n' % (cl.name,p,args[p],params.types[p]))

		fid.write("\n");
	

		#load table data
		for table,i in zip(cl.parameters.tables,range(len(cl.parameters.tables))):
			fid.write('\tmeasures_%d = %s_table_%d(%s);\n' % (i,cl.name,i,table.index))
			fid.write('\tif(measures_%d == "Error"){\n' % i)
			fid.write('\t\techo("TableLookUpError in %s, table %d");\n\t}\n' % (cl.name,i))

		fid.write('\tif(BOLTS_MODE == "bom"){\n')

		#write part name output for bom
		argc = 0
		fid.write('\t\techo(str(" "')
		for token in cl.naming.template.split():
			if token[0] == "%":
				fid.write(",")
				fid.write(args[cl.naming.substitute[argc]])
				fid.write('," "')
				argc += 1
			else:
				fid.write(',"%s"' % token)
				fid.write('," "')
		fid.write("));\n")
		#To avoid problems with missing top level object
		fid.write("\t\tcube();\n")

		fid.write("\t} else {\n")

		#module call
		fid.write('\t\t%s;\n\t}\n}\n\n' % repo.openscad.getbase[cl.id].get_incantation(args))

