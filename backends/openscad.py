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

from os import listdir,makedirs
from os.path import join, basename, dirname, exists
from shutil import copy
import re
# pylint: disable=W0622
from codecs import open
from . import license
from datetime import datetime

from .errors import *
from .common import Backend, UNITS

def get_signature(params,defaults=True):
	arg_strings = []
	for pname in params.free:
		arg_string = ''
		arg_string += pname
		if defaults:
			if params.types[pname] in ["String","Table Index"]:
					arg_string += '="%s"' % params.defaults[pname]
			elif params.types[pname] == "Bool":
				arg_string += '=%s' % str(params.defaults[pname]).lower()
			else:
				arg_string += '=%s' % params.defaults[pname]
		arg_strings.append(arg_string)
	if defaults:
		arg_strings.append('part_mode="default"')
	else:
		arg_strings.append('part_mode')
	return ', '.join(arg_strings)

def format_string(template,args):
	subs = re.compile('%\(([a-zA-z][a-z0-9_]*)\)[sd]')
	return subs.sub(lambda x: '",%s,"' % args[x.group(1)],'"%s"' % template.nice)

class OpenSCADBackend(Backend):
	def __init__(self,repo,databases):
		Backend.__init__(self,repo,"openscad",databases,["openscad"])

		#check for module name clashes
		modules = []
		#common.scad
		for mod in ["BOLTS_error", "BOLTS_warning", "BOLTS_check_dimension",
			"BOLTS_convert_to_default_unit", "get_dim", "type", "BOLTS_check_parameter_type",
			"BOLTS_thread_external", "BOLTS_hex_head", "BOLTS_hex_socket_neg"]:
			modules.append(mod)
		#conf.scad
		for mod in ["BOLTS_MODE", "BOLTS_DEFAULT_UNIT", "BOLTS_THREAD_COLOR"]:
			modules.append(mod)
		#local.scad
		for mod in ["norm", "unit_vector", "clamp", "cross_product", "almost_equal",
			"_rotation_angle", "calculate_rotation_axis", "calculate_axis", "new_cs",
			"is_orthonromal", "unit_matrix", "tensor_product_matrix3", "cross_product_matrix3",
			"rotation_matrix3", "show_cs", "translate_local", "in_cs", "align"]:
			modules.append(mod)
		#version.scad
		for mod in ["BOLTS_version", "BOLTS_date", "BOLTS_license"]:
			modules.append(mod)
		#base modules
		for module, in self.dbs["openscad"].itermodules():
			if module.name in modules:
				raise ModuleNameCollisionError(module.name)
			modules.append(module.name)
		#names
		for name, in self.dbs["openscad"].iternames():
			if name.get_id() in modules:
				raise ModuleNameCollisionError(name.get_id())
			modules.append(name.get_id())
		#standards
		for std, in self.dbs["openscad"].iterstandards():
			if std.get_id() in modules:
				raise ModuleNameCollisionError(std.get_id())
			modules.append(std.get_id())
		#classes
		for cl,module in self.dbs["openscad"].iterclasses(["class","module"]):
			params = cl.parameters.union(module.parameters)
			#tables
			for table,i in zip(params.tables,range(len(params.tables))):
				tablename = "%s_table_%s" % (cl.id,i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#2d tables
			for table,i in zip(params.tables2d,range(len(params.tables))):
				tablename = "%s_table2d_%s" % (cl.id,i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#stub module
			modulename = "%s_geo" % cl.id
			if modulename in modules:
				raise ModuleNameCollisionError(modulename)
			modules.append(modulename)
			#dim accessors
			accessorname = "%s_dims" % cl.id
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)
			#conn accessors
			accessorname = "%s_conn" % cl.id
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)
		#names
		for name,cl,module in self.dbs["openscad"].iternames(["name","class","module"]):
			params = cl.parameters.union(module.parameters)
			#tables
			for table,i in zip(params.tables,range(len(params.tables))):
				tablename = "%s_table_%s" % (name.get_id(),i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#2d tables
			for table,i in zip(params.tables2d,range(len(params.tables))):
				tablename = "%s_table2d_%s" % (name.get_id(),i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#dim accessors
			accessorname = "%s_dims" % name.get_id()
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)
			#conn accessors
			accessorname = "%s_conn" % name.get_id()
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)
		#standards
		for std,cl,module in self.dbs["openscad"].iterstandards(["standard","class","module"]):
			params = cl.parameters.union(module.parameters)
			#tables
			for table,i in zip(params.tables,range(len(params.tables))):
				tablename = "%s_table_%s" % (std.get_id(),i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#2d tables
			for table,i in zip(params.tables2d,range(len(params.tables))):
				tablename = "%s_table2d_%s" % (std.get_id(),i)
				if tablename in modules:
					raise ModuleNameCollisionError(tablename)
				modules.append(tablename)
			#dim accessors
			accessorname = "%s_dims" % std.get_id()
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)
			#conn accessors
			accessorname = "%s_conn" % std.get_id()
			if accessorname in modules:
				raise ModuleNameCollisionError(accessorname)
			modules.append(accessorname)

	def write_output(self,out_path,**kwargs):
		args = self.validate_arguments(kwargs,["target_license","version"],{"stable" : False,"expand" : False})

		self.clear_output_dir(out_path)
		#copy files
		bolts_fid = open(join(out_path,"BOLTS.scad"),"w","utf8")

		#copy common files
		if not license.is_combinable_with("LGPL 2.1+",args["target_license"]):
			raise IncompatibleLicenseError(
				"OpenSCAD common files are LGPL 2.1+, which is not compatible with %s" %
				args["target_license"]
			)
		makedirs(join(out_path,"common"))
		for filename in listdir(join(self.repo.path,"backends","openscad")):
			if not filename.endswith(".scad"):
				continue
			copy(join(self.repo.path,"backends","openscad",filename),
				join(out_path,"common",filename))
			if not args["expand"]:
				bolts_fid.write("include <common/%s>\n" % filename)
			else:
				bolts_fid.write(open(join(out_path,"common",filename)).read())

		#create version file
		version_fid = open(join(out_path,"common","version.scad"),"w","utf8")
		if args["stable"]:
			major, minor = str(args["version"]).split('.')
			version_fid.write(
				'function BOLTS_version() = [%s, %s, "%s"];\n' %
				(major, minor, target_license)
			)
		else:
			version_fid.write('function BOLTS_version() = "%s";\n' % args["version"])
		date = datetime.now()
		version_fid.write('function BOLTS_date() = [%d,%d,%d];\n' %
				(date.year, date.month, date.day))
		version_fid.write('function BOLTS_license() = "%s";\n' % args["target_license"])
		version_fid.close()
		if not args["expand"]:
			bolts_fid.write("include <common/version.scad>\n")
		else:
			bolts_fid.write(open(join(out_path,"common","version.scad")).read())

		makedirs(join(out_path,"base"))
		makedirs(join(out_path,"classes"))
		for scadfile, in self.dbs["openscad"].iterscadfiles():
			if not license.is_combinable_with(scadfile.license_name,args["target_license"]):
				continue
			#copy base files
			makedirs(join(out_path,"base",dirname(scadfile.path)))
			copy(join(self.dbs["openscad"].backend_root,scadfile.path),join(out_path,"base",scadfile.path))
			#include files
			if not args["expand"]:
				bolts_fid.write("include <base/%s>\n" % scadfile.path)
			else:
				bolts_fid.write(open(join(out_path,"base",scadfile.path)).read())

			#process classes
			for cl, module in self.dbs["openscad"].iterclasses(["class","module"],filter_scadfile = scadfile):
				with open(join(out_path,"classes","%s.scad" % cl.id),"w") as cl_fid:
					self.write_classfile(cl_fid,cl,module)
				if not args["expand"]:
					bolts_fid.write("include <classes/%s.scad>\n" % cl.id)
				else:
					bolts_fid.write(open(join(out_path,"classes","%s.scad" % cl.id)).read())

	def write_classfile(self,fid,cl,module):
		fid.write("/* Generated by BOLTS, do not modify */\n")

		params = cl.parameters.union(module.parameters)
		#write tables
		for table,i in zip(params.tables,range(len(params.tables))):
			fid.write("function %s_table_%d(idx) =\n" % (cl.id,i))
			fid.write("//%s\n" % ", ".join(table.columns))
			for k,values in table.data.items():
				data = ["None" if v is None else v for v in values]
				fid.write('idx == "%s" ? %s :\n' % (k,str(data).replace("'",'"')))
			fid.write('"Error";\n\n')

		#write 2d tables
		for table,i in zip(params.tables2d,range(len(params.tables2d))):
			fid.write("function %s_table2d_%d(rowidx,colidx) =\n" % (cl.id,i))
			for col,j in zip(table.columns,range(len(table.columns))):
				fid.write('colidx == "%s" ? %s_table2d_rows_%d(rowidx)[%d] :\n' % (col,cl.id,i,j))
			fid.write('"Error";\n\n')

			fid.write("function %s_table2d_rows_%d(rowidx) =\n" % (cl.id,i))
			for k,values in table.data.items():
				data = ["None" if v is None else v for v in values]
				fid.write('rowidx == "%s" ? %s :\n' % (k,str(data).replace("'",'"')))
			fid.write('"Error";\n\n')

		#write dim accessor
		#collect textual representations of parameters
		args = {}
		for pname in params.free:
			args[pname] = pname

		args.update(params.literal)

		for table,i in zip(params.tables,range(len(params.tables))):
			for pname,j in zip(table.columns,range(len(table.columns))):
				if params.types[pname] in UNITS:
					unit = UNITS[params.types[pname]]
					args[pname] = 'BOLTS_convert_to_default_unit(%s_table_%d(%s)[%d],"%s")' % \
						(cl.id,i,table.index,j,unit)
				else:
					args[pname] = '%s_table_%d(%s)[%d]' % (cl.id,i,table.index,j)

		for table,i in zip(params.tables2d,range(len(params.tables2d))):
			pname = table.result
			if params.types[pname] in UNITS:
				unit = UNITS[params.types[pname]]
				args[pname] = 'BOLTS_convert_to_default_unit(%s_table2d_%d(%s,%s),"%s")' % \
					(cl.id,i,table.rowindex,table.colindex,unit)
			else:
				args[pname] = '%s_table2d_%d(%s,%s)' % (cl.id,i,table.rowindex,table.colindex)

		fid.write("function %s_dims(%s) = [\n\t" % (cl.id, get_signature(params)))
		fid.write(",\n\t".join('["%s", %s]' % (pname,args[pname]) for pname in params.parameters))
		fid.write("];\n\n")

		#connector accessors
		if self.dbs["openscad"].module_connectors.contains_src(module):
			connectors = self.dbs["openscad"].module_connectors.get_dst(module)
			cargs = args.copy()
			cargs["location"] = "location"

			call = "%s(%s)" % (connectors.name, ", ".join(cargs[arg] for arg in connectors.arguments))

			fid.write("function %s_conn(location,%s) = new_cs(\n" % (cl.id, get_signature(params)))
			fid.write("\torigin=%s[0],\n\taxes=%s[1]);\n\n" % (call,call))

		#class stub
		fid.write("module %s_geo(%s){\n" % (cl.id, get_signature(params,False)))
		#module call
		dims = '%s_dims(%s)' % (cl.id,get_signature(params,False))
		fid.write('\t%s(\n\t\t' % module.name)
		fid.write(',\n\t\t'.join(['get_dim(%s,"%s")' % (dims,p) for p in module.arguments]))
		fid.write("\n\t);\n};\n\n")

		#standards
		for std, in self.dbs["openscad"].iterstandards(filter_class=cl):

			#stubs
			fid.write("module %s(%s){\n" % (std.get_id(), get_signature(params)))

			#checks
			if std.status == "withdrawn":
				fid.write('\tBOLTS_warning("The standard %s is withdrawn.' % std.get_id())
				if std.replacedby is not None:
					fid.write(
						'Although withdrawn standards are often still in use.'
						'it might be better to use its successor %s instead"' %
						(std.standard.get_nice(),std.replacedby)
					)
				fid.write('");\n')
			for pname in params.free:
				fid.write('\tBOLTS_check_parameter_type("%s","%s",%s,"%s");\n' %
					(std.get_id(),pname,args[pname],params.types[pname]))

			#bom mode
			fid.write('\tif(BOLTS_MODE == "bom"){\n')
			fid.write('\t\tif(!(part_mode == "diff")){\n')

			#write part name output for bom
			fid.write('\t\t\techo(str(%s));\n' % format_string(std.labeling,args))

			#To avoid problems with missing top level object
			fid.write("\t\t}\n")
			fid.write("\t\tcube();\n")
			fid.write("\t} else {\n")

			#module call
			fid.write('\t\t%s_geo(%s);\n' % (cl.id,get_signature(params,False)))
			fid.write("\t}\n};\n\n")

			#dims
			fid.write('function %s_dims(%s) = %s_dims(%s);\n\n' %
				(std.get_id(),get_signature(params),cl.id,get_signature(params,False)))

			#conns
			fid.write('function %s_conn(location,%s) = %s_conn(location,%s);\n\n' %
				(std.get_id(),get_signature(params),cl.id,get_signature(params,False)))

		#names
		for name, in self.dbs["openscad"].iternames(filter_class=cl):

			#stubs
			fid.write("module %s(%s){\n" % (name.get_id(), get_signature(params)))

			#checks
			for pname in params.free:
				fid.write('\tBOLTS_check_parameter_type("%s","%s",%s,"%s");\n' %
					(name.get_id(),pname,args[pname],params.types[pname]))

			#bom mode
			fid.write('\tif(BOLTS_MODE == "bom"){\n')
			fid.write('\t\tif(!(part_mode == "diff")){\n')

			#write part name output for bom
			fid.write('\t\t\techo(str(%s));\n' % format_string(name.labeling,args))

			#To avoid problems with missing top level object
			fid.write("\t\t}\n")
			fid.write("\t\tcube();\n")
			fid.write("\t} else {\n")

			#module call
			fid.write('\t\t%s_geo(%s);\n' % (cl.id,get_signature(params,False)))
			fid.write("\t}\n};\n\n")

			#dims
			fid.write('function %s_dims(%s) = %s_dims(%s);\n\n' %
				(name.get_id(),get_signature(params),cl.id,get_signature(params,False)))

			#conns
			fid.write('function %s_conn(location,%s) = %s_conn(location,%s);\n\n' %
				(name.get_id(),get_signature(params),cl.id,get_signature(params,False)))
