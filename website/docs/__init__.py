from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from os.path import exists,join
from os import listdir
from flask.helpers import safe_join, send_from_directory
from urlparse import urljoin
from website.cache import cache
from website.translation import languages, gettext_docs
from website.utils import Specification, Documentation
from docutils import core

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/docs/<version>' % ",".join(languages))

SOURCES = Documentation(join(docs.root_path,"sources"))

STABLE = SOURCES.get_stable()
DEV = SOURCES.get_dev()

SPECS = Specification(join(docs.root_path,"specs"))

@docs.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)
	if not getattr(g,'version',None) is None:
		values.setdefault('version',g.version)
	else:
		values.setdefault('version',STABLE)

@docs.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')
	g.version = values.pop('version')


@docs.route("/static/<filename>")
def static_version(filename):
	return send_from_directory(docs.static_folder,safe_join(g.version,filename))

@docs.route("/")
@docs.route("/index.html")
@cache.cached()
def index():
	if not g.version in SOURCES.get_versions():
		abort(404)
	doc_structure = {}
	for aud in SOURCES.get_audiences():
		doc_structure[aud] = {}
		for cat in SOURCES.get_categories():
			doc_structure[aud][cat] = list(SOURCES.get_documents(version=g.version,category=cat,audience=aud))
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("docs/index.html",page=page,auds=doc_structure)

@docs.route("/<cat>/<filename>")
@docs.route("/<cat>/<filename>.html")
@cache.cached()
def document(cat,filename):
	if not g.version in SOURCES.get_versions():
		abort(404)
	doc = list(SOURCES.get_documents(version=g.version,category=cat,filename=filename))
	if len(doc) != 1:
		abort(404)
	doc = doc[0].copy()
	doc["content"] = "\n\n".join(gettext_docs(p) for p in doc["content"])
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("docs/page.html",page=page,doc=doc)

@docs.route("/specification")
@docs.route("/specification.html")
@cache.cached()
def specification():
	parts = core.publish_parts(
		source=SPECS.get_version(g.version),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("docs/spec.html",page=page,content = content)

@docs.route("/changes")
@docs.route("/changes.html")
@cache.cached()
def changes():
	parts = core.publish_parts(
		source=SPECS.get_changes(),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : g.version}
	return render_template("docs/spec.html",page=page,content = content)

