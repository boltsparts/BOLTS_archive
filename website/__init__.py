from flask import Flask, render_template, abort, redirect
from flask.ext.markdown import Markdown
from flask.ext.babel import Babel,format_datetime
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.statistics import Statistics
from blog import blog

app = Flask(__name__)
app.register_blueprint(blog,url_prefix='/blog')
app.debug = True

Markdown(app)
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

@app.route("/")
@app.route("/index.html")
def hello():
	page = {"title" : "Home"}

	return render_template("home.html",page=page, stats = stats.get_statistics())

if __name__ == "__main__":
		app.run()
