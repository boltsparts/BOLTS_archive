from flask import Blueprint, render_template, abort, redirect, request, url_for
from os.path import exists,join,relpath
from yaml import safe_load as load
from os import walk, listdir

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static")

def split_yaml_header(fid):
	line = fid.readline()
	if line.strip() != '---':
		raise ValueError('No YAML header found at the beginning')
	header = []
	for line in fid:
		if line.strip() == '---':
			break
		header.append(line)
	content = '\n'.join(line for line in fid)
	return load('\n'.join(header)),content

class Documentation:
	def __init__(self,path):
		self.documents = []
		self.categories = []
		self.audiences = []

		for dirpath,_,filenames in walk(path):
			cat = relpath(dirpath,path)
			if cat == '.':
				continue
			self.categories.append(cat)

			for filename in filenames:
				doc = {}
				doc["category"] = cat
				with open(join(dirpath,filename)) as fid:
					header, content = split_yaml_header(fid)
				doc["title"] = header["title"]
				doc["filename"] = filename
				doc["audience"] = header["audience"]
				self.audiences.append(header["audience"])
				doc["content"] = content
				self.documents.append(doc)
		self.categories = list(set(self.categories))
		self.audiences = list(set(self.audiences))

	def get_categories(self):
		return self.categories

	def get_audiences(self):
		return self.audiences

	def get_documents(self,category=None,audience=None,filename=None):
		for doc in self.documents:
			if (not category is None) and doc["category"] != category:
				continue
			if (not audience is None) and doc["audience"] != audience:
				continue
			if (not filename is None) and doc["filename"] != filename:
				continue
			yield doc

SOURCES = {}
STABLE = 0
for version in listdir(join(docs.root_path,"sources")):
	try:
		STABLE = max(STABLE,float(version))
	except:
		pass
	SOURCES[version] = Documentation(join(docs.root_path,"sources",version))


@docs.route("/")
@docs.route("/index.html")
def home():
	return redirect(url_for(".index",version=STABLE))


@docs.route("/<version>")
@docs.route("/<version>/index.html")
def index(version):
	if not version in SOURCES:
		abort(404)
	src = SOURCES[version]
	doc_structure = {}
	for aud in src.get_audiences():
		doc_structure[aud] = {}
		for cat in src.get_categories():
			doc_structure[aud][cat] = list(src.get_documents(cat,aud))
	page = {"title" : "Documentation", "stable" : STABLE, "version" : version}
	return render_template("doc.html",page=page,auds=doc_structure)

@docs.route("/<version>/<cat>/<filename>")
@docs.route("/<version>/<cat>/<filename>.html")
def document(version,cat,filename):
	print version,cat,filename
	print SOURCES
	if not version in SOURCES:
		abort(404)
	src = SOURCES[version]
	print src.get_categories()
	if not cat.lower() in [cat.lower() for cat in src.get_categories()]:
		abort(404)
	doc = list(src.get_documents(cat,filename=filename))
	if len(doc) != 1:
		abort(404)
	page = {"title" : "Documentation", "stable" : STABLE, "version" : version}
	return render_template("page.html",page=page,doc=doc[0])
