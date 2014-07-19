from flask import Flask, render_template, abort, redirect
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.statistics import Statistics
from os.path import exists,join

app = Flask(__name__)
app.debug = True

repo = Repository(".")
dbs = {}
dbs["openscad"] = OpenSCADData(repo)
dbs["freecad"] = FreeCADData(repo)
dbs["drawings"] = DrawingsData(repo)

stats = Statistics(repo,dbs)

@app.route("/")
def hello():
	page = {"title" : "Home"}

	return render_template("home.html",page=page, stats = stats.get_statistics())


if __name__ == "__main__":
		app.run()
