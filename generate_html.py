from os import listdir,makedirs
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

def enclose(seq,tag):
	return ''.join("<%s>%s</%s>" % (tag,s,tag) for s in seq)

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
			args['table'] = enclose(
					[enclose(['name','description','status'],'th')] + 
					[enclose(["<a href='../parts/%s.html'>%s</a>" % (s,s),
						self.parts[s]['description'],
						self.parts[s]['status']],'td') for s in self.orgs[org]],'tr'
					)

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

#clear output
rmtree("html",True)
makedirs("html/collections")
makedirs("html/parts")
makedirs("html/organisations")

files = listdir('blt')

exporter = HTMLExporter()
for filename in files:
	if filename[-4:] == ".blt":
		print "Processing",filename
		coll = load_collection(filename)
		check_conformity(coll)
		exporter.add_collection(filename)

exporter.finish()
