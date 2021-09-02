# BOLTS - Open Library of Technical Specifications
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

from os import listdir
from os.path import dirname
from os.path import exists
from os.path import join

from .bolttools import blt
from .bolttools import pythonpackage


# import repo
rootpath = dirname(__file__)
repo = blt.Repository(rootpath)
# print(repo)
pythonpackage_db = pythonpackage.PythonPackageData(repo)


# ************************************************************************************************
# helper
def _get_default_params(cl):

    base = pythonpackage_db.base_classes.get_src(cl)
    params = cl.parameters.union(base.parameters)
    free_params = params.free

    default_params = {}
    for p in free_params:
        # p_type = params.types[p]  # not used
        default_value = params.defaults[p]
        default_params[p] = default_value
    return default_params


# ************************************************************************************************
# get information and data out of the repo

# TODO: Why are the iterators duplicated in freecad.py and openscad.py
# TODO: The yaml reader to initialize the repo seams duplicated too :-(
# TODO: are these 4 methods needed? See documentation behind these methods
# it might be much simpler be the use of the examples behind these methods ... 


def get_name(classid):
    """
    bolts.get_name()
        get SaveClassName from classid (which can be retrieved from blt file)
    """
    for n in get_names():
        name = repo.names[n]
        cl = repo.class_names.get_src(name)
        if classid == cl.id:
            return n


def get_standard(classid):
    """
    bolts.get_standard()
        get SaveStandardName from classid (which can be retrieved from blt file)
    """
    for s in get_standards():
        standard = repo.standards[s]
        cl = repo.class_standards.get_src(standard)
        if classid == cl.id:
            return s


def get_default_params_by_name(save_class_name):
    """
    bolts.get_default_params_by_name(save_class_name)
    """
    cl = repo.class_names.get_src(repo.names[save_class_name])
    return _get_default_params(cl)


def get_default_params_by_standard(save_standard_name):
    """
    bolts.get_default_params_by_standard(save_standard_name)
    """
    cl = repo.class_standards.get_src(repo.standards[save_standard_name])
    return _get_default_params(cl)


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

for it in rep.iterclasses():
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

"""
