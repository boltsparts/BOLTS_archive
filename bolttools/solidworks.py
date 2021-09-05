#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from os import listdir
from glob import iglob
from os.path import join, exists, splitext
# pylint: disable=W0622
from codecs import open

from errors import *
from common import BaseElement, DataBase, Parameters, Substitution, check_schema
from .yaml_blt_loader import load_yaml_blt


class DesignTableClass:
    def __init__(self,cl):
        check_schema(cl,"basesolidworks",
            ["classid"],
            ["naming"]
        )

        self.classid = cl["classid"]

        self.naming = Substitution(cl.get("naming",None))


class DesignTable(BaseElement):
    def __init__(self,designtable,collname,backend_root):
        BaseElement.__init__(self,designtable,collname)
        check_schema(designtable,"basesolidworks",
            ["filename","author","license","type","suffix","params","classes"],
            ["source","metadata"]
        )

        self.filename = designtable["filename"]
        self.path = join(backend_root,collname,self.filename)

        self.suffix = designtable["suffix"]

        self.outname = "%s-%s.xls" % (splitext(self.filename)[0],self.suffix)

        self.params = designtable["params"]

        self.metadata = designtable.get("metadata",{})

        self.classes = []
        for cl in designtable["classes"]:
            self.classes.append(DesignTableClass(cl))

class SolidWorksData(DataBase):
    def __init__(self,repo):
        DataBase.__init__(self,"solidworks",repo)
        self.designtables = []

        if not exists(self.backend_root):
            e = MalformedRepositoryError("solidworks directory does not exist")
            e.set_repo_path(repo.path)
            raise e

        for coll in listdir(self.backend_root):
            basefilename = join(self.backend_root,coll,"%s.base" % coll)
            if not exists(basefilename):
                #skip directory that is no collection
                continue
            base = load_yaml_blt(basefilename)
            if len(base) != 1:
                raise MalformedCollectionError(
                    "No YAML document found in file %s" % basefilename
                )
            base = base[0]

            for designtable in base:
                if not designtable["type"] == "solidworks":
                    continue
                self.designtables.append(DesignTable(designtable,coll,self.backend_root))
