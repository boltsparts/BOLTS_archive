from flask import Flask, render_template, abort, redirect, url_for
from flask.ext.babel import Babel,format_datetime
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.statistics import Statistics
from os.path import join
from blog import blog
from docs import docs
from parts import parts, repo, dbs
from . import utils, html, cms

app = Flask(__name__)
app.register_blueprint(blog,url_prefix='/blog')
app.register_blueprint(docs,url_prefix='/doc')
app.register_blueprint(parts,url_prefix='/html')
app.register_blueprint(parts,url_prefix='/parts')
app.debug = True

Babel(app)

stats = Statistics(repo,dbs)

@app.template_filter('datetime')
def _format_datetime(value, format='medium'):
	if format == 'full':
		format="EEEE, d. MMMM y 'at' HH:mm"
	elif format == 'medium':
		format="EE dd.MM.y HH:mm"
	return format_datetime(value, format)

app.jinja_env.filters['markdown_docs'] = cms.markdown_docs
app.jinja_env.filters['markdown_blog'] = cms.markdown_blog

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
