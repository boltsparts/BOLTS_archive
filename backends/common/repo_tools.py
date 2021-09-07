# BOLTS - Open Library of Technical Specifications
# Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
# Copyright (C) 2021 Bernd Hahnebach <bernd@bimstatik.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


def add_params(db_repo, repo, cl, in_params):
    # params
    if not in_params:
        in_params = get_default_params(db_repo, cl)
    all_params = add_missing_inparams(db_repo, cl, in_params)
    all_params = cl.parameters.collect(in_params)

    # add name to all_params
    if "name" not in all_params:
        name = repo.names[get_name(repo, cl.id)]
        all_params["name"] = name.labeling.get_nice(all_params)

    return all_params


def get_default_params(db_repo, cl):

    base = db_repo.base_classes.get_src(cl)
    params = cl.parameters.union(base.parameters)
    free_params = params.free

    default_params = {}
    for p in free_params:
        # p_type = params.types[p]  # not used
        default_value = params.defaults[p]
        default_params[p] = default_value
    return default_params


def add_missing_inparams(db_repo, cl, params):

    # print(cl.id)
    # print(params)
    default_params = get_default_params(db_repo, cl)
    for def_key in default_params:
        if def_key not in params:
            params[def_key] = default_params[def_key]
            print(
                "Added default parameter: {}: {}"
                .format(def_key, default_params[def_key])
            )
    return params


# ************************************************************************************************
# get information and data out of the repo


# TODO: Why are the iterators duplicated in freecad.py and openscad.py
# TODO: The yaml reader to initialize the repo seams duplicated too :-(


def get_name(repo, classid):
    for cl_name_str, cl_name_obj in repo.names.items():
        cl = repo.class_names.get_src(cl_name_obj)
        if classid == cl.id:
            return cl_name_str


def get_standard(repo, classid):
    for cl_standard_str, cl_standard_obj in repo.standards.items():
        cl = repo.class_standards.get_src(cl_standard_obj)
        if classid == cl.id:
            return cl_standard_str


"""
import BOLTS as bolts
from BOLTS import repo_tools

# or

from boltspy import repo_tools

repo_tools.get_name(bolts.repo, "ibeam_hea")
repo_tools.get_standard(bolts.repo, "ibeam_hea")
# 'HEAProfile'
# 'DIN1025_3'
"""


def get_default_params_by_name(db_repo, repo, save_class_name):
    """
    get_default_params_by_name(save_class_name)
    """
    cl = repo.class_names.get_src(repo.names[save_class_name])
    return get_default_params(db_repo, cl)


def get_default_params_by_standard(db_repo, repo, save_standard_name):
    """
    get_default_params_by_standard(save_standard_name)
    """
    cl = repo.class_standards.get_src(repo.standards[save_standard_name])
    return get_default_params(db_repo, cl)


"""
# TODO simplify !!!
# TODO default is wrong these are the default_free_params

from BOLTS.bolttools.freecad import FreeCADData
db_repo = FreeCADData(bolts.repo)

# or

from boltspy.bolttools.pythonpackage import PythonPackageData
db_repo = PythonPackageData(bolts.repo)

repo_tools.get_default_params_by_name(db_repo, bolts.repo, 'HEAProfile')
repo_tools.get_default_params_by_standard(db_repo, bolts.repo, 'DIN1025_3')

# {'type': 'HEA200', 'l': 1000, 'arch': False}
# {'type': 'HEA200', 'l': 1000, 'arch': False}

# TODO error on pythonpackage
"""


# ************************************************************************************************
# set up repo
# in BOLTS code path in a bash in Debian Buster
"""
python3 bolts.py export pythonpackage
python3

"""
# than in python shell

"""
bolts_code_path = "/home/hugo/Documents/dev/bolts/"
import sys
from os.path import join
sys.path.append(join(bolts_code_path, "BOLTS", "output", "pythonpackage"))
import boltspy as bolts

"""


# ************************************************************************************************
# acces the repo
#
# each *.blt file in data directory is a collection
# a collections consists of classes
# class and collection ids are uniqe in the entire repo
# two possibilities to access them
# the use of repo attributes or repo iterators

"""
# get the repo
repo = bolts.repo

# ***** attributes *****
# some can be used to iterate too

# all repo
sorted(list(repo.__dict__.keys()))

# collection ids
sorted(list(repo.collections.keys()))

# collection names
sorted([cl.name for cl in repo.collections.values()])

# class ids
sorted(list(repo.classes.keys()))

# class names
sorted(list(repo.names.keys()))

# standards
sorted(list(repo.standards.keys()))

# standard bodies
sorted(list(repo.bodies.keys()))


# ***** iterators *****
# found in bolttools/freecad.py and bolttools/openscad.py
# some examples

last_coll = None
for cl, coll in repo.iterclasses(["class", "collection"]):
    if coll != last_coll:
        last_coll = coll
        print(coll.id)
        print("    - ", cl.id)
    else:
        print("    - ", cl.id)

for it in repo.iterclasses():
    cl = it[0]
    print("{}:\n    - {}\n    - {}\n    - {}\n".format(cl.id, cl.url, cl.source, sorted(cl.parameters.parameters)))

for it in repo.iterclasses():
    print(sorted(list(it[0].__dict__.keys())))

for it in repo.iterclasses():
    print(sorted(list(it[0].parameters.__dict__.keys())))

for it in repo.iterclasses():
    print(it[0].id)

for cl in sorted([class_id[0].id for class_id in repo.iterclasses()]):
    cl

for it in repo.iterclasses():
    print(it[0].id)

for it in repo.iterclasses(["class"]):
    print(it[0].id)

for cl, coll in repo.iterclasses(["class", "collection"]):
    print(coll.id, " --> ", cl.id)

for name in repo.iternames():
    print(sorted(list(name[0].__dict__.keys())))

for name in repo.iternames():
    print(name[0].name.__dict__.keys())

for name in repo.iternames():
    print(name[0].name.nice)


# ***** output some part data *****

cl = repo.classes["ibeam_hea"]
# cl.parameters.tables[0].__dict__.keys()
# cl.parameters.tables[0].index
cl.parameters.tables[0].columns
# cl.parameters.tables[0].data
for k, v in cl.parameters.tables[0].data.items():
    print("{}: {}".format(k, v))


# ***** output data base object *****
db = bolts.db_repo

db.__dict__.keys()
db.name
db.repo_root
db.backend_root
db.bases

for base in db.iterbases():
    print(base)

"""
