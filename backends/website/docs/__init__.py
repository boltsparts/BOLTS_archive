from flask import Blueprint, render_template, abort, redirect, request, url_for, g, safe_join
from os.path import exists
from os import listdir
from flask.helpers import safe_join, send_from_directory
import sys
if sys.version_info.major < 3:
	from urlparse import urljoin
else:
	from urllib.parse import urljoin
from backends.website.translation import languages, gettext_docs
from backends.website.utils import Specification, Documentation
from docutils import core

docs = Blueprint("docs",__name__,template_folder="templates",static_folder="static", url_prefix='/<any(%s):lang_code>/docs' % ",".join(languages))

SOURCES = Documentation(safe_join(docs.root_path,"sources"))

STABLE = SOURCES.get_stable()
DEV = SOURCES.get_dev()

SPECS = Specification(safe_join(docs.root_path,"specs"))

@docs.url_defaults
def add_language_code(endpoint, values):
	if hasattr(g,'lang_code'):
		values.setdefault('lang_code',g.lang_code)
	else:
		values.setdefault('lang_code','en')

@docs.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

@docs.route("/<version>")
@docs.route("/<version>/index.html")
def index(version):
	if version not in SOURCES.get_versions():
		abort(404)
	doc_structure = {}
	for aud in SOURCES.get_audiences():
		doc_structure[aud] = {}
		for cat in SOURCES.get_categories():
			doc_structure[aud][cat] = list(SOURCES.get_documents(version=version,category=cat,audience=aud))
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("docs/index.html",page=page,auds=doc_structure)

@docs.route("/<version>/document/<cat>/<filename>")
@docs.route("/<version>/document/<cat>/<filename>.html")
def document(version, cat,filename):
	if version not in SOURCES.get_versions():
		abort(404)
	doc = list(SOURCES.get_documents(version=version,category=cat,filename=filename))
	if len(doc) != 1:
		abort(404)
	doc = doc[0].copy()
	doc["content"] = "\n\n".join(gettext_docs(p) for p in doc["content"])
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("docs/page.html",page=page,doc=doc)

@docs.route("/<version>/specification")
@docs.route("/<version>/specification.html")
def specification(version):
	parts = core.publish_parts(
		source=SPECS.get_version(version),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("docs/spec.html",page=page,content = content)

@docs.route("/<version>/changes")
@docs.route("/<version>/changes.html")
def changes(version):
	parts = core.publish_parts(
		source=SPECS.get_changes(),
		writer_name="html"
	)
	content = parts["body_pre_docinfo"]+parts["fragment"]
	page = {"title" : "Documentation", "stable" : str(STABLE), "dev" : str(DEV), "version" : version}
	return render_template("docs/spec.html",page=page,content = content)
