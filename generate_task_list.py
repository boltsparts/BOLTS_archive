import re
from os import listdir
import ast
from blt_parser import load_collection
import string

def enclose(seq,tag):
	return ''.join("<%s>%s</%s>" % (tag,s,tag) for s in seq)


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


files = listdir('blt')

exporter = TasksExporter()
for filename in files:
	if filename[-4:] == ".blt":
		print "Processing",filename
		coll = load_collection(filename)
		exporter.add_collection(filename)

exporter.finish()
