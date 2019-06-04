from flask import Blueprint, render_template, abort, redirect, request, url_for, g, jsonify
from backends.website.parts import repo, dbs
from backends.website.translation import parts_domain, gettext_parts, languages
from os.path import basename
import sys
if sys.version_info.major < 3:
	from urlparse import urljoin
else:
	from urllib.parse import urljoin

rest = Blueprint("rest",__name__,url_prefix='/<any(%s):lang_code>/api' % ",".join(languages))

@rest.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@rest.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

@rest.route("/ml/standard/<id>")
def ml_standard(id):
	std = repo.standards[id]
	cl = repo.class_standards.get_src(std)
	coll = repo.collection_standards.get_src(std)
	draw = dbs["drawings"].iterdimdrawings(filter_classes=cl).next()[0]

	params = cl.parameters.collect(dict(request.args.items()))

	draw_url = urljoin(request.url_root,url_for('parts.drawing',coll=coll.id,filename=basename(draw.filename) + '.png'))

	res = {
		"description" : std.description,
		"drawing" : draw_url,
		"name" : std.labeling.get_nice(params)
	}

	return jsonify(**res)

@rest.route("/ml/name/<id>")
def ml_name(id):
	name = repo.names[id]
	cl = repo.class_names.get_src(name)
	coll = repo.collection_names.get_src(name)
	draw = dbs["drawings"].iterdimdrawings(filter_classes=cl).next()[0]

	params = cl.parameters.collect(dict(request.args.items()))

	draw_url = urljoin(request.url_root,url_for('parts.drawing',coll=coll.id,filename=basename(draw.filename) + '.png'))

	res = {
		"description" : name.description,
		"drawing" : draw_url,
		"name" : name.labeling.get_nice(params)
	}

	return jsonify(**res)
