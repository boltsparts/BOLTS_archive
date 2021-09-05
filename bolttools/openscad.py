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
from os.path import join, exists
# pylint: disable=W0622
from codecs import open

from .errors import *
from .common import DataBase, BaseElement, Parameters, check_schema, Links, BijectiveLinks
from .common import check_iterator_arguments, filter_iterator_items
from .yaml_blt_loader import load_yaml_blt


class SCADFile(BaseElement):
    def __init__(self,basefile,collname):
        BaseElement.__init__(self,basefile)
        self.filename = basefile["filename"]
        self.path = join(collname,self.filename)

class SCADModule(BaseElement):
    def __init__(self,mod,basefile,collname):
        check_schema(mod,"basemodule",
            ["name", "arguments","classids"],
            ["parameters","connectors"])
        check_schema(basefile,"basemodule",
            ["filename","author","license","type","modules"],
            ["source"])

        BaseElement.__init__(self,basefile)

        self.name = mod["name"]
        self.arguments = mod["arguments"]
        self.classids = mod["classids"]

        self.parameters = Parameters(mod.get("parameters",{"types" : {}}))

class Connectors:
    def __init__(self,cs):
        check_schema(cs,"connectors",
            ["name","arguments","locations"],
            [])
        self.name = cs["name"]
        self.arguments = cs["arguments"]
        if "location" not in self.arguments:
            raise MissingLocationError(self.arguments)
        self.locations = cs["locations"]

class OpenSCADData(DataBase):
    def __init__(self,repo):
        DataBase.__init__(self,"openscad",repo)

        self.modules = []
        self.scadfiles = []
        self.connectors = []

        self.module_classes = Links()
        self.scadfile_modules = Links()
        self.collection_modules = Links()
        self.collection_scadfiles = Links()
        self.module_connectors = BijectiveLinks()

        if not exists(join(self.backend_root)):
            e = MalformedRepositoryError("openscad directory does not exist")
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
            for basefile in base:
                scadfile = SCADFile(basefile,coll)
                self.scadfiles.append(scadfile)
                self.collection_scadfiles.add_link(repo.collections[coll],scadfile)
                if basefile["type"] == "module":
                    for mod in basefile["modules"]:
                        try:
                            module = SCADModule(mod,basefile,coll)
                            self.modules.append(module)
                            self.collection_modules.add_link(repo.collections[coll],module)
                            self.scadfile_modules.add_link(scadfile,module)

                            if "connectors" in mod:
                                connectors = Connectors(mod["connectors"])
                                self.module_connectors.add_link(module,connectors)

                            for id in module.classids:
                                if id not in repo.classes:
                                    raise MalformedBaseError(
                                        "Unknown class %s" % id)
                                if self.module_classes.contains_dst(repo.classes[id]):
                                    raise NonUniqueBaseError(id)
                                self.module_classes.add_link(module,repo.classes[id])
                        except ParsingError as e:
                            e.set_base(basefile["filename"])
                            raise e
                else:
                    raise MalformedBaseError("Unknown base type %s" % basefile["type"])

    def iternames(self,items=["name"],**kwargs):
        """
        Iterator over all names of the repo.

        Possible items to request: name, multiname, collection, class, module
        """
        check_iterator_arguments(items,"name",["multiname","collection","class","module"],kwargs)

        for name,multiname,coll,cl in self.repo.iternames(["name","multiname","collection","class"]):
            its = {"name" : name, "multiname" : multiname, "collection" : coll, "class" : cl}

            if self.module_classes.contains_dst(cl):
                its["module"] = self.module_classes.get_src(cl)
                if filter_iterator_items(its,kwargs):
                    yield tuple(its[key] for key in items)

    def iterstandards(self,items=["standard"],**kwargs):
        """
        Iterator over all standards of the repo.

        Possible items to request: standard, multistandard, collection, class, module
        """
        check_iterator_arguments(items,"standard",["multistandard","collection","class","module"],kwargs)

        for standard,multistandard,coll,cl in self.repo.iterstandards(["standard","multistandard","collection","class"]):
            its = {"standard" : standard, "multistandard" : multistandard, "collection" : coll, "class" : cl}

            if self.module_classes.contains_dst(cl):
                its["module"] = self.module_classes.get_src(cl)
                if filter_iterator_items(its,kwargs):
                    yield tuple(its[key] for key in items)

    def iterclasses(self,items=["class"],**kwargs):
        """
        Iterator over all classes of the repo.

        Possible items to request: class, collection, scadfile, module
        """
        check_iterator_arguments(items,"class",["collection","scadfile","module"],kwargs)

        for cl, coll in self.repo.iterclasses(["class","collection"]):
            its = {"class" : cl, "collection" : coll}
            if self.module_classes.contains_dst(cl):
                its["module"] = self.module_classes.get_src(cl)
                its["scadfile"] = self.scadfile_modules.get_src(its["module"])
                if filter_iterator_items(its,kwargs):
                    yield tuple(its[key] for key in items)

    def itermodules(self,items=["module"],**kwargs):
        """
        Iterator over all OpenSCAD modules of the repo.

        Possible items to request: module, classes, collection
        """
        check_iterator_arguments(items,"module",["classes","collection"],kwargs)

        for module in self.modules:
            its = {"module" : module}
            its["collection"] = self.collection_modules.get_src(module)
            its["classes"] = self.module_classes.get_dsts(module)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def iterscadfiles(self,items=["scadfile"],**kwargs):
        """
        Iterator over all OpenSCAD files of the repo.

        Possible items to request: scadfile, collection
        """
        check_iterator_arguments(items,"scadfile",["collection"],kwargs)

        for sf in self.scadfiles:
            its = {"scadfile" : sf}
            its["collection"] = self.collection_scadfiles.get_src(sf)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)
