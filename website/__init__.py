from flask import Flask, render_template, abort, redirect, url_for
from flask.ext.babel import Babel,format_datetime
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.statistics import Statistics
from jinja2 import contextfilter, Markup
import markdown
import re
from os.path import join
from blog import blog
from docs import docs,STABLE
from parts import parts


app = Flask(__name__)
app.register_blueprint(blog,url_prefix='/blog')
app.register_blueprint(docs,url_prefix='/doc')
app.register_blueprint(parts,url_prefix='/html')
app.register_blueprint(parts,url_prefix='/parts')
app.debug = True

Babel(app)

repo = Repository(".")
dbs = {}
dbs["openscad"] = OpenSCADData(repo)
dbs["freecad"] = FreeCADData(repo)
dbs["drawings"] = DrawingsData(repo)

stats = Statistics(repo,dbs)

@app.template_filter('datetime')
def _format_datetime(value, format='medium'):
	if format == 'full':
		format="EEEE, d. MMMM y 'at' HH:mm"
	elif format == 'medium':
		format="EE dd.MM.y HH:mm"
	return format_datetime(value, format)

def get_subs(version):
	return {
		'doc' : lambda m: url_for('docs.document',
			version=version,
			**dict(zip(['cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'doc_version' : lambda m: url_for('docs.document',
			**dict(zip(['version','cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'blog' : lambda m: url_for('blog.post',
			**dict(zip(['year','month','day','slug'],(a.strip() for a in m.group(2).split('/'))))
		),
		'url' : lambda m: url_for(m.group(2)),
		'collection' : lambda m: 'NotImplemented',#<a href...
		'collection_url' : lambda m: 'NotImplemented',#<a href...
		'standard' : lambda m: 'NotImplemented',#'<a href="%s">%s</a>' % (m.group(2),url_for('parts.standard',m.group(2))),
		'name' : lambda m: 'NotImplemented',#'<a href="%s">%s</a>' % (m.group(2),url_for('parts.standard',m.name(2))),
		'standard_url' : lambda m: 'NotImplemented',#url_for('parts.standard',m.group(2)),
		'name_url' : lambda m: 'NotImplemented',#url_for('parts.standard',m.name(2)),
	}

def markdownsub(ctx,value,subs):
	mkd = markdown.markdown(value)
	subs = re.sub('{{\s*([^(]*)\(([^\)]*)\)\s*}}',lambda m: subs[m.group(1)](m),mkd)
	return Markup(subs)

@app.template_filter('markdown_docs')
@contextfilter
def markdown_docs(ctx,value):
	if 'page' in ctx.parent and 'version' in ctx.parent['page']:
		version = ctx.parent['page']['version']
	else:
		version = STABLE
	subs = get_subs(version)
	subs['static'] = lambda m: url_for('docs.static',filename=join(version,m.group(2)))
	return markdownsub(ctx,value,subs)

@app.template_filter('markdown_blog')
@contextfilter
def markdown_blog(ctx,value):
	if 'page' in ctx.parent and 'version' in ctx.parent['page']:
		version = ctx.parent['page']['version']
	else:
		version = str(STABLE)
	subs = get_subs(version)
	subs['static'] = lambda m: url_for('blog.static',filename=join(m.group(2)))
	return markdownsub(ctx,value,subs)


@app.route("/")
@app.route("/index.html")
def index():
	page = {"title" : "Home"}

	return render_template("home.html",page=page, stats = stats.get_statistics())

@app.route("/downloads")
@app.route("/downloads.html")
def downloads():
	page = {"title" : "Downloads"}

	return render_template("downloads.html",page=page)

@app.route("/tasks")
@app.route("/tasks.html")
def tasks():
	page = {"title" : "Contribute"}

	return render_template("tasks.html",page=page)

@app.route("/contribute")
@app.route("/contribute.html")
def contribute():
	page = {"title" : "Contribute"}

	return render_template("contribute.html",page=page)

@app.route("/contributors")
@app.route("/contributors.html")
def contributors():
	page = {"title" : "Contributors"}

	return render_template("contributors.html",page=page)

if __name__ == "__main__":
		app.run()
