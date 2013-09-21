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

from common import BackendData, BackendExporter
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

def prop_row(props,prop,value):
	props.append("<tr><th><strong>%s:</strong></th><td>%s</td></tr>" %(prop,value))

def msort(a,b):
	val_a, val_b = float(a[1:]),float(b[1:])
	if val_a < val_b:
		return -1
	elif val_a > val_b:
		return 1
	else:
		return 0

class HTMLData(BackendData):
	def __init__(self,path):
		BackendData.__init__(self,"html",path)
		self.templates = {}
		template_root = join(self.backend_root,"template")
		for filename in listdir(template_root):
			name = splitext(basename(filename))[0]
			template_path = join(template_root,filename)
			self.templates[name] = string.Template(open(template_path).read())


class HTMLExporter(BackendExporter):
	def write_output(self,repo):
		html = repo.html

		#clear output and copy files
		self.clear_output_dir(html)

		makedirs(join(html.out_root,"classes"))
		makedirs(join(html.out_root,"collections"))
		makedirs(join(html.out_root,"bodies"))

		#copy drawings
		copytree(join(repo.path,"drawings"),join(html.out_root,"drawings"))


		#write collections and parts
		for coll in repo.collections:
			self._write_collection(repo,coll)
			for cl in coll.classes:
				self._write_class(repo,coll,cl)

		for body in repo.standard_bodies:
			self._write_body(repo,body)

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

		fid = open(join(html.out_root,"index.html"),'w')
		fid.write(html.templates["index"].substitute(params))
		fid.close()


	def _write_collection(self,repo,coll):
		html = repo.html
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

		fid = open(join(html.out_root,"collections","%s.html" % coll.id),'w')
		fid.write(html.templates["collection"].substitute(params))
		fid.close()

	def _write_body(self,repo,body):
		html = repo.html
		params = {}
		params["title"] = body
		params["description"] = "Standards issued by %s" % body

		data = [["<a href='../classes/%s.html'>%s</a>" % (cl.name,cl.name),
				cl.description,
				cl.status] for cl in repo.standardized[body]]
		header = ["Name", "Description", "Status"]
		row_classes = [cl.status for cl in repo.standardized[body]]
		params["classes"] = html_table(data,header,row_classes)

		fid = open(join(html.out_root,"bodies","%s.html" % body),'w')
		fid.write(repo.html.templates["body"].substitute(params))
		fid.close()


	def _write_class(self,repo,coll,cl):
		html = repo.html
		params = {}

		params["title"] = cl.name
		params["description"] = cl.description or "No description available"
		params["drawing"] = cl.drawing or "no_drawing.png"

		props = []

		for mail,name in zip(coll.author_mails,coll.author_names):
			prop_row(props,"Author","<a href='mailto:%s'>%s</a>" % (mail,name))
		prop_row(props,"License","<a href='%s'>%s</a>" % (coll.license_url,coll.license_name))
		prop_row(props,"Collection","<a href='../collections/%s.html'>%s</a>" % (coll.id,coll.name))
		identical = ", ".join(["<a href='%s.html'>%s</a>" % (id,id) for id in cl.standard if id != cl.name])
		prop_row(props,"Identical to",identical)

		if cl.standard:
			prop_row(props,"Status",cl.status)
			prop_row(props,"Standard body","<a href='../bodies/%s.html'>%s</a>" % (cl.body,cl.body))
			if not cl.replaces is None:
				prop_row(props,"Replaces","<a href='%s.html'>%s</a>" % (cl.replaces,cl.replaces))

			if not cl.replacedby is None:
				prop_row(props,"Replaced by","<a href='%s.html'>%s</a>" % (cl.replacedby,cl.replacedby))


		if cl.url:
			prop_row(props,"Url",cl.url)
		prop_row(props,"Source",cl.source)

		params["properties"] = "\n".join(props)

		#TODO: multiple tables properly
		params["dimensions"] = ""
		for table in cl.parameters.tables:
			data = [[key] + table.data[key] for key in sorted(table.data.keys(),cmp=msort)]
			header = [str(p) for p in [table.index] + table.columns]
			params["dimensions"] += html_table(data,header)

		fid = open(join(html.out_root,"classes","%s.html" % cl.name),'w')
		fid.write(html.templates["class"].substitute(params))
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
