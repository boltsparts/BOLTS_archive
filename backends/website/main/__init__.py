from flask import Flask, render_template, abort, redirect, url_for, request, g, Blueprint
from flask.ext.babelex import gettext
from flask.helpers import send_from_directory
from bolttools.statistics import Statistics
from backends.checker import CheckerBackend
from backends.website.parts import repo, dbs
from backends.website.translation import languages
from backends.website.docs import STABLE
from backends.website.utils import Downloads
from os import environ
from os.path import join

main = Blueprint("main",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>' % ",".join(languages))

stats = Statistics(repo,dbs)
downs = Downloads(join(repo.path,"downloads"))

@main.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@main.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

@main.route("/")
@main.route("/index.html")
def index():
	page = {"title" : gettext("Home")}

	return render_template("home.html",page=page, stats = stats.get_statistics())

@main.route("/docs")
@main.route("/docs/index.html")
def docindex():
	g.version = STABLE
	return redirect(url_for("docs.index"))

@main.route("/downloads")
@main.route("/downloads.html")
def downloads():
	page = {"title" : "Downloads"}

	release = {"openscad" : {}, "freecad" : {}, "iges" : {}}


	for kind in ["stable","devel"]:
		for backend in ["openscad","freecad"]:
			release[backend][kind] = dict(zip(
				["targz","zip"],
				[downs.get_latest(backend,kind,'.tar.gz','lgpl2.1+'),
					downs.get_latest(backend,kind,'.zip','lgpl2.1+')]
			))
		for backend in ["iges"]:
			release[backend][kind] = {'tarxz' : downs.get_latest(backend,kind,'.tar.xz','none')}

	return render_template("downloads.html",page=page,release=release)

@main.route("/downloads/<path:filename>")
def files(filename):
	return send_from_directory(join(environ['OPENSHIFT_REPO_DIR'],'downloads'),filename)

@main.route("/tasks")
@main.route("/tasks.html")
def tasks():
	page = {"title" : "Contribute"}

	checker = CheckerBackend(repo,dbs)

	tables = []
	for name,task in checker.tasks.iteritems():
		tables.append({
			"title" : task.get_title(),
			"description" : task.get_description(),
			"length" : len(task.get_table()),
			"table" : website.html.table({
				"class" : "table",
				"data" : task.get_table(),
				"header" : task.get_headers()
			}),
		})

	return render_template("tasks.html",page=page,tables=tables)

@main.route("/contribute")
@main.route("/contribute.html")
def contribute():
	page = {"title" : "Contribute"}

	return render_template("contribute.html",page=page)

@main.route("/public_domain.html")
def public_domain():
	page = {"title" : "Public Domain"}

	return render_template("public_domain.html",page=page)

@main.route("/contributors")
@main.route("/contributors.html")
def contributors():
	page = {"title" : "Contributors"}

	return render_template("contributors.html",page=page,contributors = stats.get_contributors())
