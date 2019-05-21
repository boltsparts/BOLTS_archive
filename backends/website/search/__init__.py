from flask import Blueprint, render_template, abort, redirect, request, g, url_for, appcontext_pushed

import gettext

from contextlib import contextmanager

from website.parts import repo
from os import makedirs, environ
from os.path import exists, join
from shutil import rmtree
from backends.website.translation import languages, trans_dir
from backends.website.docs import SOURCES

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

import whoosh
import whoosh.fields, whoosh.index
from whoosh.analysis import LanguageAnalyzer
from whoosh.query import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.writing import AsyncWriter
from ast import literal_eval

search = Blueprint("search",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>' % ",".join(languages))

whoosh_dir = join(environ["OPENSHIFT_DATA_DIR"],'index')
if exists(whoosh_dir):
    rmtree(whoosh_dir)
makedirs(whoosh_dir)

doc_fields = {
	"category" : whoosh.fields.ID(stored=True),
	"version" : whoosh.fields.ID(stored=True),
	"url_endpoint" : whoosh.fields.ID(stored=True),
	"url_args" : whoosh.fields.ID(stored=True)
}

part_fields = {
	"category" : whoosh.fields.ID(stored=True),
	"id" : whoosh.fields.ID(field_boost=3.0,stored=True),
	"table_indices" : whoosh.fields.TEXT(),
	"url_endpoint" : whoosh.fields.ID(stored=True),
	"url_args" : whoosh.fields.ID(stored=True)
}

for lang in languages:
	doc_fields["title_%s" % lang] = whoosh.fields.TEXT(stored=True,field_boost=2.0,analyzer=LanguageAnalyzer(lang))
	doc_fields["content_%s" % lang] = whoosh.fields.TEXT(analyzer=LanguageAnalyzer(lang))

	part_fields["title_%s" % lang] = whoosh.fields.TEXT(stored=True,field_boost=2.0,analyzer=LanguageAnalyzer(lang))
	part_fields["content_%s" % lang] = whoosh.fields.TEXT(analyzer=LanguageAnalyzer(lang))


doc_schema = whoosh.fields.Schema(**doc_fields)
part_schema = whoosh.fields.Schema(**part_fields)

doc_index = whoosh.index.create_in(whoosh_dir, doc_schema, indexname="docs")
part_index = whoosh.index.create_in(whoosh_dir, part_schema, indexname="parts")

doc_parsers = {}
part_parsers = {}
for lang in languages:
    doc_parsers[lang] = MultifieldParser(['title_%s' % lang,'content_%s' % lang,'id'],schema = doc_index.schema)
    part_parsers[lang] = MultifieldParser(['title_%s' % lang,'content_%s' % lang,'id','table_indices'],schema = part_index.schema)

@search.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@search.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

@contextmanager
def lang_set(app, lang):
    def handler(sender, **kwargs):
        g.lang_code = lang
    with appcontext_pushed.connected_to(handler, app):
        yield

def rebuild_index(app):
	trans = {}
	for lang in languages:
		trans[lang] = gettext.translation('parts',trans_dir,languages=[lang], fallback=True)
	#parts
	with part_index.writer() as writer:
		for coll, in repo.itercollections():
			doc = {
				"category" : u"collection",
				"id" : unicode(coll.id),
				"url_endpoint" : u'parts.collection',
				"url_args" : unicode({"id" : coll.id})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(coll.name)
						doc["content_%s" % lang] = trans[lang].ugettext(coll.description)
			writer.add_document(**doc)
		for std,cl in repo.iterstandards(["standard","class"]):
			doc = {
				"category" : u"standard",
				"id" : unicode(std.get_id()),
				"table_indices" : u" ".join(sum(cl.parameters.choices.values(),[])),
				"url_endpoint" : u'parts.standard',
				"url_args" : unicode({"id" : std.get_id()})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(std.standard.get_nice())
						doc["content_%s" % lang] = trans[lang].ugettext(std.description)
			writer.add_document(**doc)
		for name, in repo.iternames():
			doc = {
				"category" : u"name",
				"id" : unicode(name.get_id()),
				"url_endpoint" : u'parts.name',
				"url_args" : unicode({"id" : name.get_id()})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(name.name.get_nice())
						doc["content_%s" % lang] = trans[lang].ugettext(name.description)
			writer.add_document(**doc)

	#docs
	with doc_index.writer() as writer:
		trans = {}
		for lang in languages:
			trans[lang] = gettext.translation('docs',trans_dir,languages=[lang], fallback=True)
		for doc_page in SOURCES.get_documents():
			doc = {
				"category" : unicode(doc_page["category"]),
				"version" : unicode(doc_page["version"]),
				"url_endpoint" : u"docs.document",
				"url_args" : unicode({
					"cat" : doc_page["category"],
					"filename" : doc_page["filename"],
					"version" : doc_page["version"]
				})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(doc_page["title"])
						doc["content_%s" % lang] = "\n\n".join(
							trans[lang].ugettext(p) for p in doc_page["content"])
			writer.add_document(**doc)

class SearchForm(Form):
    query = TextField("query",validators=[DataRequired()])

@search.route("/search",methods=('GET','POST'))
def search_page():
    results = None
    query = request.args.get('q','')
    form = SearchForm()

    if query == '':
        if form.validate_on_submit():
            return redirect(url_for('search.search_page',q=form.query.data))
    else:
	results = {"parts" : [], "docs" : []}
	with part_index.searcher() as searcher:
		hits = searcher.search(part_parsers[g.lang_code].parse(query))
		for hit in hits:
			res = {
				'title' : hit['title_%s' % g.lang_code],
				'url' : url_for(hit['url_endpoint'],**literal_eval(hit['url_args'])),
				'category' : hit['category']
			}
			results["parts"].append(res)
	with doc_index.searcher() as searcher:
		hits = searcher.search(doc_parsers[g.lang_code].parse(query))
		for hit in hits:
			res = {
				'title' : hit['title_%s' % g.lang_code],
				'url' : url_for(hit['url_endpoint'],**literal_eval(hit['url_args'])),
				'version' : hit['version'],
				'category' : hit['category']
			}
			results["docs"].append(res)
	
    page = {'title' : 'Search'}
    return render_template('search.html', page=page,form=form,query=query,results=results)


