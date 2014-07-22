from flask import Blueprint, render_template, abort, redirect, request
from os.path import join
from os import environ
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData


parts = Blueprint("parts",__name__,template_folder="templates")

repo = Repository(environ['OPENSHIFT_REPO_DIR'])
dbs = {
	"freecad" : FreeCADData(repo),
	"openscad" : OpenSCADData(repo),
	"drawings" : DrawingsData(repo)
}

@parts.route('/')
def index():
	collections = [{'id' : coll.id, 'name' : coll.name} for coll, in repo.itercollections()]
	bodies = [ body.body for body, in repo.iterbodies()]
	page = {"title" : "Part list"}
	return render_template("index.html",page=page,collections=collections,bodies=bodies)

@parts.route('/collections/<id>')
@parts.route('/collections/<id>.html')
def collection(id):
	coll = repo.collections[id]
	return "Eimer"

@parts.route('/bodies/<id>')
@parts.route('/bodies/<id>.html')
def body(id):
	coll = repo.bodies[id]
	return "Eimer"

@parts.route('/thingtracker')
@parts.route('/thingtracker.json')
def thingtracker():
	return abort(404)
