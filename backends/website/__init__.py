from flask import Flask, render_template, abort, redirect, url_for, request, g
from flask_babelex import Babel,format_datetime, gettext, lazy_gettext
from flask_assets import Bundle, Environment
from os.path import exists
from os import environ, makedirs, getenv
from shutil import rmtree
from .blog import blog
from .docs import docs
from .main import main
from .parts import parts
from .rest import rest
from . import cms
from . import translation
import logging


app = Flask(__name__)

assets = Environment(app)

assets.register('css',Bundle('source/style.less',depends='source/*.less',filters=['less','cleancss']),output='css/style.css')
assets.register('js',Bundle('js/jquery-2.1.1.min.js','js/bootstrap.min.js'),output='js/all.js')

app.register_blueprint(main)
app.register_blueprint(blog)
app.register_blueprint(docs)
app.register_blueprint(parts)
app.register_blueprint(rest)

babel = Babel(app,default_domain=translation.messages_domain)

app.jinja_env.filters['markdown_docs'] = cms.markdown_docs
app.jinja_env.filters['markdown_blog'] = cms.markdown_blog
app.jinja_env.globals['gettext_parts'] = translation.gettext_parts
app.jinja_env.globals['gettext_docs'] = translation.gettext_docs

@babel.localeselector
def get_locale():
	lang_code = getattr(g,'lang_code',None)
	if lang_code is None:
		lang_code = 'en'
	return lang_code

@app.errorhandler(404)
def error_404(e):
	g.lang_code = get_locale()
	return render_template('error.html',
		page={'title' : 'Page not found'},
		title=gettext('Page not found (404)'),
		message=gettext('The page you are looking for does not exist. Maybe you made a mistake while typing the URL')
	), 404

@app.errorhandler(500)
def error_500(e):
	g.lang_code = get_locale()
	return render_template('error.html',
		page={'title' : 'Server Error'},
		title=gettext('Something went wrong (500)'),
		message=gettext('An error happened while processing your request. This should not happen, we are very sorry. Please tell us about the this problem by sending a mail to BOLTS@ist-dein-freund.de and include the URL you were trying to access.')
	), 500


@app.route("/")
@app.route("/index.html")
def index():
	# page = {"title" : gettext("Home")}  # not used
	return render_template("redirect.html", url = url_for("main.index", lang_code=get_locale()))


if __name__ == "__main__":
	app.run()
