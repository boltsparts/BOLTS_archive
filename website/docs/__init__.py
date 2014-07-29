from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from os.path import exists,join
from os import listdir
from flask.helpers import safe_join, send_from_directory
from urlparse import urljoin
from ..cache import cache
from ..translation import languages
from ..utils import Specification, Documentation

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/docs' % ",".join(languages))

@docs.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@docs.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

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

