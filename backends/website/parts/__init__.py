from flask import Blueprint, render_template, abort, redirect, request, url_for, g
from flask_babelex import gettext, ngettext
from flask.helpers import safe_join, send_from_directory
from os.path import split
from os import environ
from bolttools.blt import Repository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from backends.openscad import get_signature
from .. import html
from .. import utils
from backends.website.translation import parts_domain, gettext_parts, languages

parts = Blueprint("parts",__name__,template_folder="templates",url_prefix='/<any(%s):lang_code>/parts' % ",".join(languages))

@parts.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@parts.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')


import backends
repo = Repository(split(split(backends.__file__)[0])[0])
dbs = {
	"freecad" : FreeCADData(repo),
	"openscad" : OpenSCADData(repo),
	"drawings" : DrawingsData(repo)
}

def get_identical_links(cl,prt):
	identical = []
	if repo.class_standards.contains_src(cl):
		for s in repo.class_standards.get_dsts(cl):
			if s is prt:
				continue
			identical.append(html.a(s.standard.get_nice(),href=url_for('.standard',id=s.get_id())))
	if repo.class_names.contains_src(cl):
		for n in repo.class_names.get_dsts(cl):
			if n is prt:
				continue
			identical.append(html.a(gettext_parts(n.name.get_nice()),href=url_for('.name',id=n.get_id())))
	return identical

def format_author_prop(author_list):
	return (ngettext('Author','Authors',len(author_list)),', '.join(author_list))

@parts.route('/')
@parts.route('/index.html')
def index():
	collections = [{'id' : coll.id, 'name' : coll.name} for coll, in repo.itercollections()]
	bodies = [body.body for body, in repo.iterbodies()]
	page = {"title" : "Part list"}
	return render_template("parts/index.html",page=page,collections=collections,bodies=bodies)

@parts.route('/drawings/<coll>/<filename>')
def drawing(filename,coll):
	return send_from_directory(safe_join(repo.path,'drawings'),safe_join(coll,filename))

@parts.route('/collections/<id>')
@parts.route('/collections/<id>.html')
def collection(id):
	coll = repo.collections[id]
	names = []
	for name, in repo.iternames(filter_collection=coll):
		names.append({
			'name' : name.name.get_nice(),
			'id' : name.get_id(),
			'description' : name.description
		})
	standards = []
	for std, in repo.iterstandards(filter_collection=coll):
		standards.append({
			'standard' : std.standard.get_nice(),
			'id' : std.get_id(),
			'description' : std.description
		})
	page = {"title" : "Part list"}

	#Properties
	props = []
	props.append(format_author_prop(coll.author_names))
	props.append((gettext('License'),html.a(coll.license_name,href=coll.license_url)))
	props.append(('ID',coll.id))
	return render_template("parts/collection.html",
		page=page,
		coll=coll,
		standards=sorted(standards, key=lambda x: x["id"]),
		names=sorted(names, key=lambda x: x["id"]),
		props=html.properties(props)
	)

@parts.route('/bodies/<id>')
@parts.route('/bodies/<id>.html')
def body(id):
	body = repo.bodies[id]
	standards = []
	for std, in repo.iterstandards(filter_body=body):
		standards.append({
			'standard' : std.standard.get_nice(),
			'id' : std.get_id(),
			'description' : std.description
		})
	page = {"title" : "Part list"}
	return render_template("parts/body.html",page=page,body=body,standards=standards)

@parts.route('/standards/<id>')
@parts.route('/standards/<id>.html')
def standard(id):
	std = repo.standards[id]
	cl = repo.class_standards.get_src(std)
	coll = repo.collection_standards.get_src(std)

	#properties
	props = []
	props.append(format_author_prop(coll.author_names))
	props.append((gettext('License'),html.a(coll.license_name,href=coll.license_url)))
	props.append((gettext('Collection'),html.a(coll.name,href=url_for('.collection',id=coll.id))))

	identical = get_identical_links(cl,std)
	if len(identical) > 0:
		props.append((gettext('Identical to'),', '.join(identical)))

	props.append((gettext('Status'),std.status))
	props.append((gettext('Standard body'),html.a(std.body,href=url_for('.body',id=std.body))))
	if std.replaces is not None:
		props.append((gettext('Replaces'),std.replaces))
	if std.replacedby is not None:
		props.append((gettext('Replaced by'),std.replacedby))
	if not cl.url == "":
		props.append(('URL',cl.url))
	props.append(('ID',std.get_id()))
	props.append((gettext('Source'),cl.source))

	#parameters
	parameters = {}
	parameters["tables"] = []
	for table in utils.tables_as_dicts(cl.parameters):
		table["class"] = "table"
		parameters["tables"].append(html.table(table))

	parameters["tables2d"] = []
	for table in utils.tables2d_as_dicts(cl.parameters):
		table["class"] = "table"
		parameters["tables2d"].append(html.table2d(table))

	parameters["drawing"] = None
	if dbs["drawings"].dimdrawing_classes.contains_dst(cl):
		draw = dbs["drawings"].dimdrawing_classes.get_src(cl)
		parameters["drawing"] = url_for('.drawing',coll=coll.id,filename = "%s.png" % draw.filename)

	parameters["description"] = html.table({
		"header" : [gettext("Parameter Name"),gettext("Description")],
		"data" : [[p,gettext_parts(cl.parameters.description[p])] for p in cl.parameters.parameters],
		"class" : "table"
	})

	#freecad
	freecad = {}
	if dbs["freecad"].base_classes.contains_dst(cl):
		base = dbs["freecad"].base_classes.get_src(cl)

		freecad["props"] = []
		freecad["props"].append(format_author_prop(base.author_names))
		freecad["props"].append((gettext('License'),html.a(base.license_name,href=base.license_url)))
		freecad["props"] = html.properties(freecad["props"])

	#openscad
	openscad = {}
	if dbs["openscad"].module_classes.contains_dst(cl):
		module = dbs["openscad"].module_classes.get_src(cl)

		openscad["props"] = []
		openscad["props"].append(format_author_prop(module.author_names))
		openscad["props"].append((gettext('License'),html.a(module.license_name,href=module.license_url)))
		openscad["props"] = html.properties(openscad["props"])

		params = cl.parameters.union(module.parameters)
		openscad["incantation_module"] = "module %s(%s)" % (std.get_id(),get_signature(params))
		openscad["incantation_dims"] = "function %s_dims(%s)" % (std.get_id(),get_signature(params))
		openscad["incantation_conn"] = "function %s_conn(location,%s)" % (std.get_id(),get_signature(params))

		if dbs["openscad"].module_connectors.contains_src(module):
			connectors = dbs["openscad"].module_connectors.get_dst(module)
			conns = []
			for loc in connectors.locations:
				if not dbs["drawings"].conlocations_condrawings.contains_src(loc):
					continue
				for draw in dbs["drawings"].conlocations_condrawings.get_dsts(loc):
					if cl in dbs["drawings"].condrawings_classes.get_dsts(draw):
						draw_url = url_for('.drawing',coll=coll.id,filename = "%s.png" % draw.filename)
						conns.append([loc,html.a(html.img(src=draw_url,width="200"),href=draw_url)])

			openscad["connectors"] = html.table({
				"header" : [gettext("Location"),gettext("Drawing")],
				"class" : "table",
				"data" : conns
			})
		else:
			openscad["connectors"] = None

	page = {"title" : "Part list"}
	return render_template(
		"parts/standard.html",
		page = page,
		std = std,
		props = html.properties(props),
		parameters = parameters,
		freecad = freecad,
		openscad = openscad
	)

@parts.route('/names/<id>')
@parts.route('/names/<id>.html')
def name(id):
	name = repo.names[id]
	cl = repo.class_names.get_src(name)
	coll = repo.collection_names.get_src(name)

	#properties
	props = []
	props.append(format_author_prop(coll.author_names))
	props.append((gettext('License'),html.a(coll.license_name,href=coll.license_url)))
	props.append((gettext('Collection'),html.a(coll.name,href=url_for('.collection',id=coll.id))))

	identical = get_identical_links(cl,name)
	if len(identical) > 0:
		props.append((gettext('Identical to'),', '.join(identical)))

	if not cl.url == "":
		props.append(('URL',cl.url))
	props.append(('ID',name.get_id()))
	props.append((gettext('Source'),cl.source))

	#parameters
	parameters = {}
	parameters["tables"] = []
	for table in utils.tables_as_dicts(cl.parameters):
		table["class"] = "table"
		parameters["tables"].append(html.table(table))

	parameters["tables2d"] = []
	for table in utils.tables2d_as_dicts(cl.parameters):
		table["class"] = "table"
		parameters["tables2d"].append(html.table2d(table))

	parameters["drawing"] = None
	if dbs["drawings"].dimdrawing_classes.contains_dst(cl):
		draw = dbs["drawings"].dimdrawing_classes.get_src(cl)
		parameters["drawing"] = url_for('.drawing',coll=coll.id,filename = "%s.png" % draw.filename)

	parameters["description"] = html.table({
		"header" : [gettext("Parameter Name"),gettext("Description")],
		"data" : [[p,gettext_parts(cl.parameters.description[p])] for p in cl.parameters.parameters],
		"class" : "table"
	})

	#freecad
	freecad = {}
	if dbs["freecad"].base_classes.contains_dst(cl):
		base = dbs["freecad"].base_classes.get_src(cl)

		freecad["props"] = []
		freecad["props"].append(format_author_prop(base.author_names))
		freecad["props"].append((gettext('License'),html.a(base.license_name,href=base.license_url)))
		freecad["props"] = html.properties(freecad["props"])
	else:
		freecad = None

	#openscad
	openscad = {}
	if dbs["openscad"].module_classes.contains_dst(cl):
		module = dbs["openscad"].module_classes.get_src(cl)

		openscad["props"] = []
		openscad["props"].append(format_author_prop(module.author_names))
		openscad["props"].append((gettext('License'),html.a(module.license_name,href=module.license_url)))
		openscad["props"] = html.properties(openscad["props"])

		params = cl.parameters.union(module.parameters)
		openscad["incantation_module"] = "module %s(%s)" % (name.get_id(),get_signature(params))
		openscad["incantation_dims"] = "function %s_dims(%s)" % (name.get_id(),get_signature(params))
		openscad["incantation_conn"] = "function %s_conn(location,%s)" % (name.get_id(),get_signature(params))

		if dbs["openscad"].module_connectors.contains_src(module):
			connectors = dbs["openscad"].module_connectors.get_dst(module)
			conns = []
			for loc in connectors.locations:
				if not dbs["drawings"].conlocations_condrawings.contains_src(loc):
					continue
				for draw in dbs["drawings"].conlocations_condrawings.get_dsts(loc):
					if cl in dbs["drawings"].condrawings_classes.get_dsts(draw):
						draw_url = url_for('.drawing',coll=coll.id,filename = "%s.png" % draw.filename)
						conns.append([loc,html.a(html.img(src=draw_url,width="200"),href=draw_url)])

			openscad["connectors"] = html.table({
				"header" : [gettext("Location"),gettext("Drawing")],
				"class" : "table",
				"data" : conns
			})
		else:
			openscad["connectors"] = None
	else:
		openscad = None

	page = {"title" : "Part list"}
	return render_template(
		"parts/name.html",
		page = page,
		name = name,
		props = html.properties(props),
		parameters = parameters,
		freecad = freecad,
		openscad = openscad
	)
