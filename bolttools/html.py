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

from os import listdir,makedirs
import re
from os.path import join, exists, basename,splitext
from shutil import rmtree,copytree
import string

#inspired by html.py but avoiding the dependency

def html_table(table_data,header=None,row_classes=None):
	"generates the content of a html table without the surrounding table tags"
	res = []
	if not header is None:
		row = " ".join(["<th>%s</th>" % str(head) for head in header])
		res.append("<tr>%s<tr>" % row)
	if row_classes is None:
		row_classes = [None]*len(table_data)
	for row_data,row_class in zip(table_data,row_classes):
		row = " ".join(["<td>%s</td>" % str(datum) for datum in row_data])
		if row_class is None:
			res.append("<tr>%s</tr>" % row)
		else:
			res.append("<tr class='%s'>%s</tr>" % (row_class,row))
	return "\n".join(res)

def msort(a,b):
	val_a, val_b = float(a[1:]),float(b[1:])
	if val_a < val_b:
		return -1
	elif val_a > val_b:
		return 1
	else:
		return 0

class HTMLData:
	def __init__(self,path):
		self.templates = {}
		for filename in listdir(join(path,"html","template")):
			name = splitext(basename(filename))[0]
			self.templates[name] = string.Template(open(join(path,"html","template",filename)).read())



class HTMLExporter:
	def write_output(self,repo):
		self.repo = repo
		self.out_path = join(repo.path,"output","html")

		#clear output and copy files
		rmtree(self.out_path,True)

		makedirs(self.out_path)
		makedirs(join(self.out_path,"classes"))
		makedirs(join(self.out_path,"collections"))
		makedirs(join(self.out_path,"bodies"))


		#write collections and parts
		for coll in repo.collections:
			self._write_collection(coll)
			for cl in coll.classes:
				self._write_class(coll,cl)

		for body in repo.standard_bodies:
			self._write_body(body)

		#write index
		params = {}
		params["title"] = "BOLTS Index"
		data = [["<a href='collections/%s.html'>%s</a>" % (coll.id,coll.name), coll.description]
				for coll in repo.collections]
		header = ["Name", "Description"]
		params["collections"] = html_table(data,header)
		data = [["<a href='bodies/%s.html'>%s</a>" % (body,body), "Standards issued by %s" % body]
				for body in repo.standard_bodies]
		header = ["Name", "Description"]
		params["bodies"] = html_table(data,header)

		fid = open(join(self.out_path,"index.html"),'w')
		fid.write(self.repo.html.templates["index"].substitute(params))
		fid.close()


	def _write_collection(self,coll):
		params = {}
		params["title"] = coll.name
		params["description"] = coll.description or "No description available"

		params["author"] = " and <br>".join(["<a href='mailto:%s'>%s</a>" % (m,n) \
				for m,n in zip(coll.author_mails,coll.author_names)])

		params["license"] = "<a href='%s'>%s</a>" % (coll.license_url,coll.license_name)

		data = [["<a href='../classes/%s.html'>%s</a>" % (cl.name,cl.name),
				cl.description,
				cl.status] for cl in coll.classes]
		header = ["Name", "Description", "Status"]
		row_classes = [cl.status for cl in coll.classes]
		params["classes"] = html_table(data,header,row_classes)

		fid = open(join(self.out_path,"collections","%s.html" % coll.id),'w')
		fid.write(self.repo.html.templates["collection"].substitute(params))
		fid.close()

	def _write_body(self,body):
		params = {}
		params["title"] = body
		params["description"] = "Standards issued by %s" % body

		data = [["<a href='../classes/%s.html'>%s</a>" % (cl.name,cl.name),
				cl.description,
				cl.status] for cl in self.repo.standardized[body]]
		header = ["Name", "Description", "Status"]
		row_classes = [cl.status for cl in  self.repo.standardized[body]]
		params["classes"] = html_table(data,header,row_classes)

		fid = open(join(self.out_path,"bodies","%s.html" % body),'w')
		fid.write(self.repo.html.templates["body"].substitute(params))
		fid.close()


	def _write_class(self,coll,cl):
		params = {}
		params["title"] = cl.name
		params["author"] = " and <br>".join(["<a href='mailto:%s'>%s</a>" % (m,n) \
				for m,n in zip(coll.author_mails,coll.author_names)])
		params["license"] = "<a href='%s'>%s</a>" % (coll.license_url,coll.license_name)
		params["description"] = cl.description or "No description available"
		params["collection"] = "<a href='../collections/%s.html'>%s</a>" % (coll.id,coll.name)
		params["identical"] = ", ".join(["<a href='%s.html'>%s</a>" % (id,id) \
				for id in cl.standard if id != cl.name])
		params["status"] = cl.status if cl.standard else ""
		params["body"] = "<a href='../bodies/%s.html'>%s</a>" % (cl.body,cl.body) or ""
		params["url"] = cl.url or ""
		params["source"] = cl.source
		params["drawing"] = cl.drawing

		params["replaces"] = ""
		if not cl.replaces is None:
			params["replaces"] = "<a href='%s.html'>%s</a>" % (cl.replaces,cl.replaces) or ""

		params["replacedby"] = ""
		if not cl.replacedby is None:
			params["replacedby"] = "<a href='%s.html'>%s</a>" % (cl.replacedby,cl.replacedby)

		#TODO: multiple tables properly
		params["dimensions"] = ""
		for table in cl.parameters.tables:
			data = [[key] + table.data[key] for key in sorted(table.data.keys(),cmp=msort)]
			header = [str(p) for p in [table.index] + table.columns]
			params["dimensions"] += html_table(data,header)

		fid = open(join(self.out_path,"classes","%s.html" % cl.name),'w')
		fid.write(self.repo.html.templates["class"].substitute(params))
		fid.close()

#class TasksExporter:
#	def __init__(self):
#		self.tasks_template = string.Template(open("template/tasks.html").read())
#
#		#this is super-fragile base parsing using regular expressions
#		#better approach would be a proper parser for openscad and importing the module
#		#and checking the bases dict for freecad
#		self.scad_re = re.compile('module (?P<base>[a-z_0-9]*)\((?P<params>([a-zA-Z_0-9]*[, ]{0,2})*)\){')
#		self.python_re = re.compile('def (?P<base>[a-z_0-9]*)\(params, ?document\):')
#
#		#bases referenced in the blt files and their parameters
#		self.blt_bases = []
#		self.blt_params = []
#
#		#find all bases found in the scad files and their parameters
#		self.scad_bases = []
#		self.scad_params = []
#
#		#freecad bases, there we have no possibility of finding parameters
#		self.freecad_bases = []
#
#	def add_collection(self,filename):
#
#		coll = load_collection(filename)
#		for base in coll['scad']['base-functions']:
#			self.blt_bases.append(base)
#			self.blt_params.append(coll['scad']['base-functions'][base])
#
#	def finish(self):
#
#		#find scad bases
#		for filename  in listdir('scad'):
#			if filename in ['common.scad','conf.scad','sketch.scad']:
#				continue
#			for line in open('scad/' + filename):
#				match = self.scad_re.match(line)
#				if match is None:
#					continue
#				basename = match.group(1)
#				if basename.endswith('_sketch'):
#					continue
#				self.scad_bases.append(match.group('base'))
#				self.scad_params.append(match.group('params'))
#
#		#find freecad bases
#		for filename in listdir('freecad'):
#			for line in open('freecad/' + filename):
#				match = self.python_re.match(line)
#				if match is None:
#					continue
#				self.freecad_bases.append(match.group('base'))
#
#		#write html
#		content = {}
#		content['basetable'] = enclose(
#				[enclose(['base','OpenSCAD','FreeCAD'],'th')] +
#				[enclose([base,base in self.scad_bases, base in self.freecad_bases],'td') for base in self.blt_bases],'tr')
#		with open('html/tasks.html','w') as fid:
#			fid.write(self.tasks_template.substitute(content))
#
