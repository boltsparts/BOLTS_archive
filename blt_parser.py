import yaml

_specification = { 0.1: {
	"root" : (["collection","parts"],["scad"]),
	"collection" : (["author","license","blt-version"],["name","description"]),
	"scad" : (["base-file","base-functions"],[]),
	"part" : (["standard","name","base","target-args"],["status","replaces","description","literal-args","url","table","notes"]),
	"name" : (["template"],["parameters"]),
	"table" : (["columns","data"],[])
	},
}

_defaults = { 0.1: {
	"part" : [("status","active")],
	},
}

_unify = { 0.1: {
	"scad" : ["base-file"],
	"part" : ["standard","replaces"]
	}
}

def check_dict(array,name,spec):
	man = spec[0][:]
	opt = spec[1][:]
	for key in array.keys():
		if key in man:
			man.remove(key)
		elif key in opt:
			opt.remove(key)
		else:
			print "Warning! Unknown field in %s: %s" % (name,key)
	if len(man) > 0:
		print "Error! Missing mandatory fields in %s: %s" % (name,man)

def check_conformity(coll):
	version = coll["collection"]["blt-version"]
	if not version in _specification.keys():
		print "Error! Unknown Version:",version
	spec = _specification[version]
	check_dict(coll,"root",spec["root"])
	check_dict(coll["collection"],"collection",spec["collection"])
	if "scad" in coll.keys():
		check_dict(coll["scad"],"scad",spec["scad"])
	parts = coll["parts"]
	for part,i in zip(parts,range(len(parts))):
		check_dict(part,"part%d"%i,spec["part"])
		if "table" in part.keys():
			check_dict(part["table"],"table",spec["table"])

def set_defaults(coll):
	version = coll["collection"]["blt-version"]
	default = _defaults[version]
	for part in coll["parts"]:
		for key,value in default["part"]:
			if not key in part.keys():
				part[key] = value

def unify_to_list(coll):
	"""Replace fields that can be both name or list by lists to ease access"""
	version = coll["collection"]["blt-version"]
	unify = _unify[version]
	for field in unify["scad"]:
		if field in coll["scad"] and isinstance(coll["scad"][field],str):
			coll["scad"][field] = [coll["scad"][field]]

	for part in coll["parts"]:
		for field in unify["part"]:
			if field in part and isinstance(part[field],str):
				part[field] = [part[field]]


def load_collection(filename):
	coll = list(yaml.load_all(open("blt/" + filename)))[0]
	check_conformity(coll)
	set_defaults(coll)
	unify_to_list(coll)
	return coll
	
