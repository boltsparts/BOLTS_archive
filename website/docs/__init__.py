from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from os.path import exists,relpath, splitext, join
from flask.helpers import safe_join, send_from_directory
from yaml import safe_load as load
from urlparse import urljoin
from os import walk, listdir
from ..cache import cache
import re
from docutils import core
from ..translation import languages

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/docs' % ",".join(languages))

@docs.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@docs.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')


def split_yaml_header(fid):
	line = fid.readline()
	if line.strip() != '---':
		raise ValueError('No YAML header found at the beginning')
	header = []
	for line in fid:
		if line.strip() == '---':
			break
		header.append(line)
	content = ''.join(line for line in fid)
	return load('\n'.join(header)),content

class Specification:
	def __init__(self,path):
		self.version = {}
		self.changes = open(join(path,"changes.rst")).read()

		spec_pattern = re.compile("blt_spec_([0-9]\.[0-9])\.rst")

		for filename in listdir(path):
			match = spec_pattern.match(filename)
			if not match is None:
				self.version[match.group(1)] = open(join(path,filename)).read()
	def get_version(self,version):
		return self.version[version]
	def get_changes(self):
		return self.changes

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
				if filename.startswith('.'):
					continue
				doc = {}
				doc["category"] = cat
				with open(join(dirpath,filename)) as fid:
					header, content = split_yaml_header(fid)
				doc["title"] = header["title"]
				doc["filename"] = splitext(filename)[0]
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
		res = []
		for doc in self.documents:
			if (not category is None) and doc["category"] != category:
				continue
			if (not audience is None) and doc["audience"] != audience:
				continue
			if (not filename is None) and doc["filename"] != filename:
				continue
			res.append(doc)
		return res

SOURCES = {}
versions = []
for version in listdir(join(docs.root_path,"sources")):
	try:
		versions.append(float(version))
	except:
		pass
	SOURCES[version] = Documentation(join(docs.root_path,"sources",version))
versions.sort()

STABLE = versions[-2]
DEV = versions[-1]

SPECS = Specification(join(docs.root_path,"specs"))

@docs.route("/static/<version>/<filename>")
def static_version(version,filename):
	return send_from_directory(docs.static_folder,safe_join(version,filename))

@docs.route("/")
@docs.route("/index.html")
def index():
	return redirect(url_for(".version_index",version=STABLE))

@docs.route("/<version>")
@docs.route("/<version>/index.html")
@cache.cached()
def version_index(version):
	if not version in SOURCES:
		return abort(404)
	src = SOURCES[version]
	doc_structure = {}
	for aud in src.get_audiences():
		doc_structure[aud] = {}
		for cat in src.get_categories():
			doc_structure[aud][cat] = list(src.get_documents(category=cat,audience=aud))
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("doc.html",page=page,auds=doc_structure)

@docs.route("/<version>/<cat>/<filename>")
@docs.route("/<version>/<cat>/<filename>.html")
@cache.cached()
def document(version,cat,filename):
	if not version in SOURCES:
		return abort(404)
	src = SOURCES[version]
	doc = list(src.get_documents(category=cat,filename=filename))
	if len(doc) != 1:
		return abort(404)
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("page.html",page=page,doc=doc[0])

@docs.route("/<version>/specification")
@docs.route("/<version>/specification.html")
@cache.cached()
def specification(version):
	parts = core.publish_parts(
		source=SPECS.get_version(version),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("spec.html",page=page,content = content)

@docs.route("/changes")
@docs.route("/changes.html")
@cache.cached()
def changes():
	parts = core.publish_parts(
		source=SPECS.get_changes(),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("spec.html",page=page,content = content)

