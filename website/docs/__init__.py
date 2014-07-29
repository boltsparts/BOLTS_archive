from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from os.path import exists,join
from os import listdir
from flask.helpers import safe_join, send_from_directory
from urlparse import urljoin
from ..cache import cache
from ..translation import languages
from ..utils import Specification, Documentation

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/docs/<version>' % ",".join(languages))

@docs.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)
	values.setdefault('version',g.version)

@docs.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')
	g.version = values.pop('version')

SOURCES = Documentation(join(docs.root_path,"sources"))

STABLE = SOURCES.get_stable()
DEV = SOURCES.get_dev()

SPECS = Specification(join(docs.root_path,"specs"))

@docs.route("/static/<filename>")
def static_version(filename):
	return send_from_directory(docs.static_folder,safe_join(g.version,filename))

@docs.route("/")
@docs.route("/index.html")
@cache.cached()
def version_index():
	if not g.version in SOURCES.get_versions():
		return abort(404)
	doc_structure = {}
	for aud in SOURCES.get_audiences():
		doc_structure[aud] = {}
		for cat in SOURCES.get_categories():
			doc_structure[aud][cat] = list(SOURCES.get_documents(version=g.version,category=cat,audience=aud))
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("doc.html",page=page,auds=doc_structure)

@docs.route("/<cat>/<filename>")
@docs.route("/<cat>/<filename>.html")
@cache.cached()
def document(cat,filename):
	if not g.version in SOURCES.get_versions():
		return abort(404)
	doc = list(SOURCES.get_documents(version=g.version,category=cat,filename=filename))
	if len(doc) != 1:
		return abort(404)
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("page.html",page=page,doc=doc[0])

@docs.route("/specification")
@docs.route("/specification.html")
@cache.cached()
def specification():
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

