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
import os.path
from shutil import rmtree,copytree
from blt_parser import load_collection, check_conformity
import string

def msort(a,b):
	val_a, val_b = float(a[1:]),float(b[1:])
	if val_a < val_b:
		return -1
	elif val_a > val_b:
		return 1
	else:
		return 0

def enclose(seq,tag,cls=None):
	if cls is None:
		return ''.join('<%s>%s</%s>' % (tag,s,tag) for s in seq)
	else:
		return ''.join('<%s class="%s">%s</%s>' % (tag,c,s,tag) for s,c in zip(seq,cls))

class HTMLExporter:
	def __init__(self):
		self.collections = {}
		self.collection_template = string.Template(open("template/collection.html").read())
		self.orgs = {}
		self.org_template = string.Template(open("template/org.html").read())
		self.parts = {}
		self.part_template = string.Template(open("template/part.html").read())
		self.index_template = string.Template(open("template/index.html").read())

	def add_collection(self,filename):
		blt = load_collection(filename)
		coll = blt['collection']

		path,bltname = os.path.split(filename)
		base,ext = os.path.splitext(bltname)

		args = {}

		args['title'] = coll['name']

		if 'description' in coll:
			args['description'] = coll['description']
		else:
			args['description'] = ''

		args['author'] = coll['author']
		if '<' in args['author'] and '>' in args['author']:
			name,mail = args['author'].split('<')
			args['author'] = "<a href='mailto:%s'>%s</a>" % (mail[:-1].strip(),name.strip())

		args['license'] = coll['license']
		if '<' in args['license'] and '>' in args['license']:
			name,url = args['license'].split('<')
			args['license'] = "<a href='%s'>%s</a>" % (url[:-1].strip(),name.strip())

		args['parts'] = []
		for part in blt['parts']:
			standards = part['standard']
			for standard in standards:
				args['parts'].append(
					"<tr class='%s'> <td><a href='../parts/%s.html'>%s</a></td> <td>%s</td> <td>%s</td> </tr>" %
						(part['status'] or 'active', standard, standard, part['description'], part['status'])
				)
		args['parts'] = "\n".join(args['parts'])

		self.collections[base] = args

		#generate part pages
		for part in blt['parts']:
			self._add_part(part,blt,base,args['license'])


	def _add_part(self,part,collection,collname,license):
		for standard in part['standard']:
			args = {}

			args['title'] = standard

			args['identical'] = " ".join(["<a href='%s.html'>%s</a>" % (p,p) for p in part['standard'] if not p == standard])

			#find standardisation organisation
			args['org'] = None
			for i in range(len(standard)):
				if not standard[i].isalpha():
					args['org'] = standard[:i]
					break

			args['status'] = part['status']

			if 'replaces' in part:
				args['replaces'] = part['replaces']
			else:
				args['replaces'] = ''

			args['description'] = part['description']

			#will be filled in finish
			args['replacedby'] = ''

			if 'url' in part:
				args['url'] = "<a href=%s>%s</a>" % (part['url'],part['url'])
			else:
				args['url'] = ''

			if 'notes' in part:
				args['notes'] = part['notes']
			else:
				args['notes'] = ''

			args['table'] = enclose(
				[enclose([''] + part['table']['columns'],'th')] +
				[enclose([r] + part['table']['data'][r],'td') for r in sorted(part['table']['data'],cmp=msort)],
				'tr')

			args['collection'] = "<a href='../collections/%s.html'>%s</a>" % (collname,collection['collection']['name'])
			args['author'] = collection['collection']['author']

			args['license'] = license

			args['drawing'] = part['base']

			self.parts[standard] = args

	def finish(self):
		for part in self.parts:
			#add replacements
			replaceds = self.parts[part]['replaces']
			for replaced in replaceds:
				if replaced in self.parts:
					self.parts[replaced]['replacedby'] = part

			#add standards
			if not self.parts[part]['org'] in self.orgs:
				self.orgs[self.parts[part]['org']] = []
			self.orgs[self.parts[part]['org']].append(part)


		for part in self.parts:
			#convert part references to links
			self.parts[part]['replaces'] = "".join(["<a href='../parts/%s.html'>%s</a> " % (r,r) for r in self.parts[part]['replaces']])

			self.parts[part]['replacedby'] = "<a href='../parts/%s.html'>%s</a> " % (self.parts[part]['replacedby'],self.parts[part]['replacedby'])

			org = self.parts[part]['org']
			self.parts[part]['org'] = "<a href='../organisations/%s.html'>%s</a> " % (org,org)

			#write parts files
			fid = open('html/parts/%s.html' % part,'w')
			fid.write(self.part_template.substitute(self.parts[part]))
			fid.close()

		for org in self.orgs:
			args = {}
			args['parts'] = ['<tr><th>Name</ts><th>Description</th><th>Status</th>']
			for s in self.orgs[org]:
				args['parts'].append('<tr class="%s"><td><a href="../parts/%s.html">%s</a></td><td>%s</td><td>%s</td>' % (self.parts[s]['status'],s,s,self.parts[s]['description'],self.parts[s]['status']))
			args['parts'] = "\n".join(args['parts'])

			args['title'] = org
			fid = open('html/organisations/%s.html' % org,'w')
			fid.write(self.org_template.substitute(args))
			fid.close()

		for coll in self.collections:
			fid = open('html/collections/%s.html' % coll,'w')
			fid.write(self.collection_template.substitute(self.collections[coll]))
			fid.close()

		#index file
		fid = open('html/index.html','w')
		args = {}
		args['title'] = 'BOLTS Index'
		args['collections'] = "<br>".join(["<a href='collections/%s.html'>%s</a>" % (k,self.collections[k]['title']) for k in self.collections])

		args['organisations'] = "<br>".join(["<a href='organisations/%s.html'>%s</a>" % (k,k) for k in self.orgs])

		fid.write(self.index_template.substitute(args))
		fid.close()

class TasksExporter:
	def __init__(self):
		self.tasks_template = string.Template(open("template/tasks.html").read())

		#this is super-fragile base parsing using regular expressions
		#better approach would be a proper parser for openscad and importing the module
		#and checking the bases dict for freecad
		self.scad_re = re.compile('module (?P<base>[a-z_0-9]*)\((?P<params>([a-zA-Z_0-9]*[, ]{0,2})*)\){')
		self.python_re = re.compile('def (?P<base>[a-z_0-9]*)\(params, ?document\):')

		#bases referenced in the blt files and their parameters
		self.blt_bases = []
		self.blt_params = []

		#find all bases found in the scad files and their parameters
		self.scad_bases = []
		self.scad_params = []

		#freecad bases, there we have no possibility of finding parameters
		self.freecad_bases = []

	def add_collection(self,filename):

		coll = load_collection(filename)
		for base in coll['scad']['base-functions']:
			self.blt_bases.append(base)
			self.blt_params.append(coll['scad']['base-functions'][base])

	def finish(self):

		#find scad bases
		for filename  in listdir('scad'):
			if filename in ['common.scad','conf.scad','sketch.scad']:
				continue
			for line in open('scad/' + filename):
				match = self.scad_re.match(line)
				if match is None:
					continue
				basename = match.group(1)
				if basename.endswith('_sketch'):
					continue
				self.scad_bases.append(match.group('base'))
				self.scad_params.append(match.group('params'))

		#find freecad bases
		for filename in listdir('freecad'):
			for line in open('freecad/' + filename):
				match = self.python_re.match(line)
				if match is None:
					continue
				self.freecad_bases.append(match.group('base'))

		#write html
		content = {}
		content['basetable'] = enclose(
				[enclose(['base','OpenSCAD','FreeCAD'],'th')] +
				[enclose([base,base in self.scad_bases, base in self.freecad_bases],'td') for base in self.blt_bases],'tr')
		with open('html/tasks.html','w') as fid:
			fid.write(self.tasks_template.substitute(content))

#clear output
rmtree("html",True)
makedirs("html/collections")
makedirs("html/parts")
makedirs("html/organisations")

files = listdir('blt')

pages = HTMLExporter()
tasks = TasksExporter()
for filename in files:
	if filename[-4:] == ".blt":
		print "Processing",filename
		coll = load_collection(filename)
		check_conformity(coll)
		pages.add_collection(filename)
		tasks.add_collection(filename)

pages.finish()
tasks.finish()

#generate downloads 
download_template = string.Template(open("template/downloads.html").read())
content = {}
content['devdistopenscad'] = sorted(listdir('downloads/openscad'))[-1]
content['devdistfreecad'] = sorted(listdir('downloads/freecad'))[-1]
content['devdisthtml'] = sorted(listdir('downloads/html'))[-1]

with open('html/downloads.html','w') as fid:
	fid.write(download_template.substitute(content))


