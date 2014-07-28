from flask import Flask, render_template, abort, redirect, url_for, request
from flask.ext.babelex import Babel,format_datetime, gettext, lazy_gettext, Domain
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.statistics import Statistics
from os.path import join, exists
from os import environ, makedirs
from shutil import rmtree
from cache import cache
import translation
from blog import blog
from docs import docs
from parts import parts, repo, dbs
from . import utils, html, cms

app = Flask(__name__)

cachedir = join(environ["OPENSHIFT_DATA_DIR"],"cache")
#clear cache
if exists(cachedir):
	rmtree(cachedir)
makedirs(cachedir)

app.config['CACHE_DIR'] = cachedir

#set timeout to about a month, as content only changes on push, and we clear
#the cache then. This results in a lazy static site generator
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3000000

cache.init_app(app)

app.register_blueprint(blog,url_prefix='/blog')
app.register_blueprint(docs,url_prefix='/doc')
#for compatibility with old links
app.register_blueprint(parts,url_prefix='/html')
app.register_blueprint(parts,url_prefix='/parts')
app.debug = True

babel = Babel(app,default_domain=translation.messages_domain)

stats = Statistics(repo,dbs)

app.jinja_env.filters['markdown_docs'] = cms.markdown_docs
app.jinja_env.filters['markdown_blog'] = cms.markdown_blog
app.jinja_env.globals['gettext_parts'] = translation.gettext_parts

@babel.localeselector
def get_locale():
	#the four most popular languages from the website
	return request.accept_languages.best_match(['en','es','de','fr'])

@app.route("/")
@app.route("/index.html")
@cache.cached()
def index():
	page = {"title" : lazy_gettext("Home")}

	return render_template("home.html",page=page, stats = stats.get_statistics())

@app.route("/downloads")
@app.route("/downloads.html")
@cache.cached()
def downloads():
	page = {"title" : "Downloads"}

	return render_template("downloads.html",page=page)

@app.route("/tasks")
@app.route("/tasks.html")
@cache.cached()
def tasks():
	page = {"title" : "Contribute"}

	return render_template("tasks.html",page=page)

@app.route("/contribute")
@app.route("/contribute.html")
@cache.cached()
def contribute():
	page = {"title" : "Contribute"}

	return render_template("contribute.html",page=page)

@app.route("/contributors")
@app.route("/contributors.html")
@cache.cached()
def contributors():
	page = {"title" : "Contributors"}

	return render_template("contributors.html",page=page)

if __name__ == "__main__":
		app.run()
