from flask import Blueprint, render_template, abort, redirect, request, g, url_for, appcontext_pushed

import gettext

from contextlib import contextmanager

from ..parts import repo
from os import makedirs, environ
from os.path import exists, join
from shutil import rmtree
from ..translation import languages, trans_dir
from ..docs import SOURCES

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

search = Blueprint("search",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/search' % ",".join(languages))

whoosh_dir = join(environ["OPENSHIFT_DATA_DIR"],'index')
if exists(whoosh_dir):
    rmtree(whoosh_dir)
makedirs(whoosh_dir)

fields = {
	"facet" : whoosh.fields.ID(stored=True),
	"category" : whoosh.fields.ID(stored=True),
	"id" : whoosh.fields.ID(stored=True),
	"version" : whoosh.fields.ID(stored=True),
	"url_endpoint" : whoosh.fields.ID(stored=True),
	"url_args" : whoosh.fields.ID(stored=True)
}

for lang in languages:
	fields["title_%s" % lang] = whoosh.fields.TEXT(stored=True,analyzer=LanguageAnalyzer(lang))
	fields["content_%s" % lang] = whoosh.fields.TEXT(stored=True,analyzer=LanguageAnalyzer(lang))

schema = whoosh.fields.Schema(**fields)
index = whoosh.index.create_in(whoosh_dir, schema)
parsers = {}
for lang in languages:
    parsers[lang] = MultifieldParser(['title_%s' % lang,'content_%s' % lang,'id'],schema = index.schema)

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
	with index.writer() as writer:
		#parts
		for coll, in repo.itercollections():
			doc = {
				"facet" : u"parts",
				"category" : u"collection",
				"id" : unicode(coll.id),
				"url_endpoint" : u'parts.collection',
				"url_args" : unicode({"id" : coll.id})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(coll.name),
						doc["content_%s" % lang] = trans[lang].ugettext(coll.description)
			writer.add_document(**doc)
		for std, in repo.iterstandards():
			doc = {
				"facet" : u"parts",
				"category" : u"standard",
				"id" : unicode(std.get_id()),
				"url_endpoint" : u'parts.standard',
				"url_args" : unicode({"id" : std.get_id()})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(std.standard.get_nice()),
						doc["content_%s" % lang] = trans[lang].ugettext(std.description)
			writer.add_document(**doc)
		for name, in repo.iternames():
			doc = {
				"facet" : u"parts",
				"category" : u"name",
				"id" : unicode(name.get_id()),
				"url_endpoint" : u'parts.name',
				"url_args" : unicode({"id" : name.get_id()})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(name.name.get_nice()),
						doc["content_%s" % lang] = trans[lang].ugettext(name.description)
			writer.add_document(**doc)

		#docs
		trans = {}
		for lang in languages:
			trans[lang] = gettext.translation('docs',trans_dir,languages=[lang], fallback=True)
		for doc_page in SOURCES.get_documents():
			doc = {
				"facet" : u"docs",
				"category" : unicode(doc_page["category"]),
				"version" : unicode(doc_page["version"]),
				"url_endpoint" : u"docs.document",
				"url_args" : unicode({"cat" : doc_page["category"], "filename" : doc_page["filename"]})
			}
			for lang in languages:
				with lang_set(app,lang):
					with app.app_context() as c:
						doc["title_%s" % lang] = trans[lang].ugettext(doc_page["title"]),
						doc["content_%s" % lang] = "\n\n".join(
							trans[lang].ugettext(p) for p in doc_page["content"])
			writer.add_document(**doc)

class SearchForm(Form):
    query = TextField("query",validators=[DataRequired()])

@search.route("/",methods=('GET','POST'))
def search_page():
    results = None
    query = request.args.get('q','')
    form = SearchForm()

    if query == '':
        if form.validate_on_submit():
            return redirect(url_for('search.search_page',q=form.query.data))
    else:
	results = []
	with index.searcher() as searcher:
		hits = searcher.search(parsers[g.lang_code].parse(query))
		for i in range(hits.scored_length()):
		    results.append({
			'title' : hits[i]['title_%s' % g.lang_code][0],
			'content' : hits[i]['content_%s' % g.lang_code][0],
			'url' : url_for(hits[i]['url_endpoint'],**literal_eval(hits[i]['url_args'])),
			'facet' : hits[i]['facet'],
			'category' : hits[i]['category']
		    })
    page = {'title' : 'Search'}
    return render_template('search.html', page=page,form=form,query=query,results=results)


