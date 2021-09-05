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

from .errors import *
from .common import BaseElement, DataBase, Parameters, check_schema, Links, BipartiteLinks
from .common import check_iterator_arguments, filter_iterator_items
from .yaml_blt_loader import load_yaml_blt

class Drawing(BaseElement):
    def __init__(self,basefile,collname,backend_root):
        BaseElement.__init__(self,basefile)
        self.filename = basefile["filename"]
        #TODO: move this out so that collname and backend_root can be dropped
        self.path = join(backend_root,collname,self.filename)

        self.versions = {}
        for version in iglob(self.path + ".*"):
            ext = splitext(version)[1][1:]
            self.versions[ext] = version

    def get_png(self):
        if "png" not in self.versions:
            return None
        return self.versions["png"]

    def get_svg(self):
        if "svg" not in self.versions:
            return None
        return self.versions["svg"]

class DrawingDimensions(Drawing):
    def __init__(self,basefile,collname,backend_root):
        check_schema(basefile,"drawing",
            ["filename","author","license","type","classids"],
            ["source"]
        )
        Drawing.__init__(self,basefile,collname,backend_root)

class DrawingConnectors(Drawing):
    def __init__(self,basefile,collname,backend_root):
        check_schema(basefile,"drawing",
            ["filename","author","license","type","classids","location"],
            ["source"]
        )
        Drawing.__init__(self,basefile,collname,backend_root)

        self.location = basefile["location"]

class DrawingsData(DataBase):
    def __init__(self,repo):
        DataBase.__init__(self,"drawings", repo)
        self.dimdrawings = []
        self.condrawings = []
        self.conlocations = []

        self.dimdrawing_classes = Links()
        self.condrawings_classes = BipartiteLinks()
        self.conlocations_condrawings = BipartiteLinks()

        self.collection_dimdrawings = Links()
        self.collection_condrawings = Links()

        if not exists(join(self.backend_root)):
            e = MalformedRepositoryError("drawings directory does not exist")
            e.set_repo_path(path)
            raise e

        for coll in listdir(self.backend_root):
            basefilename = join(self.backend_root,coll,"%s.base" % coll)
            if not exists(basefilename):
                #skip directory that is no collection
                continue
            if coll not in repo.collections:
                raise MalformedRepositoryError(
                    "Drawings for unknown collection found: %s " % coll)

            base_info = load_yaml_blt(basefilename)
            if len(base_info) != 1:
                raise MalformedCollectionError(
                    "Not exactly one YAML document found in file %s" % basefilename)
            base_info = base_info[0]

            for drawing_element in base_info:
                if drawing_element["type"] == "drawing-dimensions":
                    draw = DrawingDimensions(drawing_element,coll,self.backend_root)
                    if draw.get_svg() is None and draw.get_png() is None:
                        raise MalformedRepositoryError("No drawing files present for %s/%s" % (coll,draw.filename))

                    self.dimdrawings.append(draw)

                    if drawing_element["classids"] == []:
                        raise MalformedBaseError("Drawing with no associated classes found")
                    for id in drawing_element["classids"]:
                        self.dimdrawing_classes.add_link(draw,self.repo.classes[id])
                    self.collection_dimdrawings.add_link(repo.collections[coll],draw)
                if drawing_element["type"] == "drawing-connector":
                    draw = DrawingConnectors(drawing_element,coll,self.backend_root)
                    if draw.get_svg() is None and draw.get_png() is None:
                        raise MalformedRepositoryError("No drawing files present for %s/%s" % (coll,draw.filename))

                    if draw.location not in self.conlocations:
                        self.conlocations.append(draw.location)
                    self.conlocations_condrawings.add_link(draw.location,draw)

                    self.condrawings.append(draw)
                    for id in drawing_element["classids"]:
                        self.condrawings_classes.add_link(draw,self.repo.classes[id])
                    self.collection_condrawings.add_link(repo.collections[coll],draw)

    def iterclasses(self,items=["class"],**kwargs):
        """
        Iterator over all classes of the repo.

        Possible items to request: class, collection, dimdrawing, condrawings
        """
        check_iterator_arguments(items,"class",["collection","dimdrawing","condrawings"],kwargs)

        for cl,coll in self.repo.iterclasses(["class","collection"]):
            its = {"class" : cl, "collection" : coll}
            if self.condrawings_classes.contains_dst(cl):
                its["condrawings"] = self.condrawings_classes.get_srcs(cl)
            else:
                its["condrawings"] = []
            if self.dimdrawing_classes.contains_dst(cl):
                its["dimdrawing"] = self.dimdrawing_classes.get_src(cl)
            else:
                its["dimdrawing"] = None

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def iterdimdrawings(self,items=["dimdrawing"],**kwargs):
        """
        Iterator over all dimension drawings of the repo.

        Possible items to request: dimdrawing, classes, collection
        """
        check_iterator_arguments(items,"dimdrawing",["classes", "collection"],kwargs)

        for draw in self.dimdrawings:
            its = {"dimdrawing" : draw}
            its["collection"] = self.collection_dimdrawings.get_src(draw)
            its["classes"] = self.dimdrawing_classes.get_dsts(draw)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def itercondrawings(self,items=["condrawing"],**kwargs):
        """
        Iterator over all connector drawings of the repo.

        Possible items to request: condrawing, conlocations, classes, collection
        """
        check_iterator_arguments(items,"condrawing",["conlocations", "classes", "collection"],kwargs)

        for draw in self.condrawings:
            its = {"condrawing" : draw}
            its["collection"] = self.collection_condrawings.get_src(draw)
            its["classes"] = self.condrawings_classes.get_dsts(draw)
            its["conlocations"] = self.conlocations_condrawings.get_srcs(draw)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)
