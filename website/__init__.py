from flask import Flask, render_template, abort, redirect
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from os.path import exists,join

app = Flask(__name__)
app.debug = True

repo = Repository(".")
dbs = {}
dbs["openscad"] = OpenSCADData(repo)
dbs["freecad"] = FreeCADData(repo)
dbs["drawings"] = DrawingsData(repo)


@app.route("/")
def hello():
	return "Hello World! Size of repo"

@app.route("/name/<id>")
def show_name(id):
	
	coll = repo.collection_names.get_src(repo.names[id])
	return coll.name


if __name__ == "__main__":
		app.run()
