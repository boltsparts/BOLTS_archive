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

import string
import os
from os.path import splitext, exists, join
# pylint: disable=W0622
from codecs import open

from .errors import *
from .common import Links, Parameters, Identifier, Substitution, parse_angled, check_schema
from .common import check_iterator_arguments, filter_iterator_items
from .yaml_blt_loader import load_yaml_blt

CURRENT_VERSION = 0.4


class Designation:
    """
    Base class for python classes to refer to a BOLTS class.
    """
    def __init__(self):
        pass
    def get_id(self):
        raise NotImplementedError

class ClassName(Designation):
    """
    Python class to provide a name for a BOLTS class, corresponding to a
    ClassNameElement in the blt file.
    """
    def __init__(self,cn):
        check_schema(cn,"classname",
            ["name","labeling"],
            ["description","group"]
        )
        Designation.__init__(self)

        try:
            if isinstance(cn['name'],str):
                self.name = Identifier({'nice' : cn['name']})
            else:
                self.name = Identifier(cn['name'])
            if isinstance(cn['labeling'],str):
                self.labeling = Substitution({'nice' : cn['labeling']})
            else:
                self.labeling = Substitution(cn['labeling'])
        except ParsingError as e:
            e.set_class(self.id)
            raise e

        self.description = cn.get('description','')

        if 'group' in cn:
            if isinstance(cn['group'],str):
                self.group = Identifier({'nice' : cn['group']})
            else:
                self.group = Identifier(cn['group'])
        else:
            self.group = Identifier({'nice' : ""})

    def get_id(self):
        return self.name.get_safe()

class ClassStandard(Designation):
    """
    Python class to provide a standard name for a BOLTS class, corresponding to a
    ClassStandardElement in the blt file.
    """
    def __init__(self,sn):
        check_schema(sn,'classstandard',
            ['standard','labeling','body'],
            ['group','year','status','replaces','description']
        )
        Designation.__init__(self)

        if isinstance(sn['standard'],str):
            self.standard = Identifier({'nice' : sn['standard']})
        else:
            self.standard = Identifier(sn['standard'])
        if 'group' in sn:
            if isinstance(sn['group'],str):
                self.group = Identifier({'nice' : sn['group']})
            else:
                self.group = Identifier(sn['group'])
        else:
            self.group = Identifier({'nice' : ""})
        if isinstance(sn['labeling'],str):
            self.labeling = Substitution({'nice' : sn['labeling']})
        else:
            self.labeling = Substitution(sn['labeling'])

        self.body = sn['body']
        self.year = sn.get('year',None)
        self.status = sn.get('status','active')

        self.replacedby = None

        self.replaces = sn.get('replaces',None)
        self.description = sn.get('description','')

    def get_id(self):
        return self.standard.get_safe()

class Class:
    """
    Python class representing a BOLTS class. There is no direct
    correspondence between a class in the blt file and this python class,
    some aspects are covered by other classes
    """
    def __init__(self,cl):
        check_schema(cl,"class",
            ["source","id"],
            ["names","standards","parameters","url","notes"]
        )

        self.id = cl["id"]

        try:
            self.parameters = Parameters(cl.get("parameters",{"types" : {}}))
        except ParsingError as e:
            e.set_class(self.id)
            raise e

        self.url = cl.get("url","")
        self.notes = cl.get("notes","")

        self.source = cl["source"]

class Collection:
    """
    Container for all classes contained in a BOLTS Collection
    """
    def __init__(self,coll):
        check_schema(coll,"collection",
            ["id","author","license","blt-version","classes"],
            ["name","description"]
        )

        version = coll["blt-version"]
        if version != CURRENT_VERSION:
            raise VersionError(version)

        self.id = coll["id"]

        self.name = coll.get("name","")
        self.description = coll.get("description","")

        self.authors = coll["author"]
        if isinstance(self.authors,str):
            self.authors = [self.authors]

        self.author_names = []
        self.author_mails = []
        for author in self.authors:
            match = parse_angled(author)
            self.author_names.append(match[0])
            self.author_mails.append(match[1])

        self.license = coll["license"]
        match = parse_angled(self.license)
        self.license_name = match[0]
        self.license_url = match[1]

class StandardBody:
    """
    Container for standard names that are specified by a common
    standardisation body
    """
    def __init__(self,body):
        self.body = body

class MultiStandard(Designation):
    """
    Container for all standard names that are covered by a single standard
    """
    def __init__(self,standard):
        Designation.__init__(self)

        self.standard = standard

    def get_id(self):
        return self.standard.get_safe()

class MultiName(Designation):
    """
    Container for class names that are closely related, e.g. variations of a part
    """
    def __init__(self,group):
        Designation.__init__(self)

        self.group = group
    def get_id(self):
        return self.group.get_safe()

class Repository:
    def __init__(self,path):
        #check for conformity
        if not exists(path):
            e = MalformedRepositoryError("Repo directory does not exist")
            e.set_repo_path(path)
            raise e
        if not exists(join(path,"data")):
            e = MalformedRepositoryError("No data directory found")
            e.set_repo_path(path)
            raise e

        self.path = path

        #objects that have an id
        self.classes = {}
        self.collections = {}
        self.names = {}
        self.standards = {}
        self.multinames = {}
        self.multistandards = {}
        self.bodies = {}

        #relations
        self.class_names = Links()
        self.class_standards = Links()
        self.multiname_names = Links()
        self.multistandard_standards = Links()
        self.body_standards = Links()
        self.body_multistandards = Links()
        self.collection_classes = Links()
        self.collection_standards = Links()
        self.collection_multistandards = Links()
        self.collection_names = Links()
        self.collection_multinames = Links()
        self.standard_replaced = Links(1)

        #load collection data
        for filename in os.listdir(join(path,"data")):
            if splitext(filename)[1] != ".blt":
                continue
            raw_coll = load_yaml_blt(join(path, "data", filename))
            if len(raw_coll) == 0:
                raise MalformedCollectionError(
                    "No YAML document found in file %s" % filename)
            if len(raw_coll) > 1:
                raise MalformedCollectionError(
                    "More than one YAML document found in file %s" % filename)
            #we only consider the first YAML document
            raw_coll = raw_coll[0]

            if not isinstance(raw_coll["classes"],list):
                raise MalformedCollectionError("No class in collection %s" % raw_coll["id"])

            if raw_coll["id"] in self.collections:
                raise MalformedCollectionError("Duplicate collection id %s" % raw_coll["id"])

            if raw_coll["id"] != splitext(filename)[0]:
                raise MalformedCollectionError(
                    "Collection ID is not identical with file name: %s" % filename)
            for c in raw_coll["id"]:
                if c not in string.ascii_letters + string.digits + "_":
                    raise MalformedCollectionError(
                        "Collection ID contains invalid character: %s" % c)

            try:
                coll = Collection(raw_coll)
                self.collections[coll.id] = coll
            except ParsingError as e:
                e.set_repo_path(path)
                e.set_collection(filename)
                raise e

            for cl in raw_coll['classes']:

                if cl["id"] in self.classes:
                    raise MalformedRepositoryError("Duplicate class id %s" % cl["id"])

                try:
                    cls = Class(cl)
                    self.classes[cls.id] = cls
                except ParsingError as e:
                    e.set_class(cl["id"])
                    e.set_repo_path(path)
                    e.set_collection(filename)
                    raise e

                self.collection_classes.add_link(coll,cls)

                names = []
                standards = []
                if 'names' in cl:
                    if isinstance(cl['names'],list):
                        names = cl['names']
                    else:
                        names = [cl['names']]
                if 'standards' in cl:
                    if isinstance(cl['standards'],list):
                        standards = cl['standards']
                    else:
                        standards = [cl['standards']]

                if len(names+standards) == 0:
                    raise MalformedCollectionError(
                        "Encountered class with no names: %s" % raw_coll["id"])

                for cn in names:
                    try:
                        name = ClassName(cn)
                    except ParsingError as e:
                        e.set_class(cls.id)
                        raise e
                    if name.get_id() in self.names:
                        raise MalformedRepositoryError("Duplicate name %s" % name.get_id())

                    self.names[name.get_id()] = name
                    self.class_names.add_link(cls,name)

                    multinameid = name.group.get_safe()
                    if multinameid:
                        if multinameid not in self.multinames:
                            multiname = MultiName(name.group)
                            self.multinames[multinameid] = multiname
                        else:
                            multiname = self.multinames[multinameid]
                        self.collection_multinames.add_link(coll,multiname)
                        self.multiname_names.add_link(multiname,name)
                    else:
                        self.collection_names.add_link(coll,name)

                for sn in standards:
                    try:
                        standard = ClassStandard(sn)
                    except ParsingError as e:
                        e.set_class(cls.id)
                        raise e

                    if standard.get_id() in self.standards:
                        raise MalformedRepositoryError("Duplicate standard %s" % standard.get_id())

                    self.standards[standard.get_id()] = standard
                    self.class_standards.add_link(cls,standard)

                    bodyid = standard.body
                    if bodyid in self.bodies:
                        body = self.bodies[bodyid]
                    else:
                        body = StandardBody(bodyid)
                        self.bodies[bodyid] = body

                    self.body_standards.add_link(body,standard)
                    self.collection_standards.add_link(coll,standard)

                    multistdid = standard.group.get_safe()
                    if multistdid:
                        if multistdid not in self.multistandards:
                            multistd = MultiStandard(standard.group)
                            self.multistandards[multistdid] = multistd
                            self.body_multistandards.add_link(body,multistd)
                            self.collection_multistandards.add_link(coll,multistd)
                        else:
                            multistd = self.multistandards[multistdid]

                        self.multistandard_standards.add_link(multistd,standard)

        for standard in self.standards.values():
            if standard.replaces is not None:
                if standard.replaces not in self.standards:
                    raise MalformedRepositoryError(
                        "Unknown replace field %s in standard %s" %
                        (standard.replaces,standard.get_id())
                    )
                self.standard_replaced.add_link(standard,self.standards[standard.replaces])

    def iternames(self,items=["name"],**kwargs):
        """
        Iterator over all names of the repo.

        Possible items to request: name, multiname, collection, class
        """
        check_iterator_arguments(items,"name",["multiname","collection","class"],kwargs)

        '''
        for name in self.names.values():
        '''
        # use following two lines instead, to get the names sorted
        for n in sorted(self.names):
            name = self.names[n]

            its = {"name" : name}
            its["class"] = self.class_names.get_src(name)
            if self.multiname_names.contains_dst(name):
                its["multiname"] = self.multiname_names.get_src(name)
                its["collection"] = self.collection_multinames.get_src(multiname)
            else:
                its["multiname"] = None
                its["collection"] = self.collection_names.get_src(name)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def itermultinames(self,items=["multiname"],**kwargs):
        """
        Iterator over all multinames of the repo.

        Possible items to rerquest: multiname, names, collection
        """
        check_iterator_arguments(items,"multiname",["names","collection"],kwargs)

        for mname in self.multinames.values():
            its = {"multiname" : mname}
            its["names"] = self.multiname_names.get_dsts(mname)
            its["collection"] = self.collection_multinames.get_src(mname)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def iterstandards(self,items=["standard"],**kwargs):
        """
        Iterator over all standards of the repo.

        Possible items to request: standard, multistandard, body, collection, class
        """
        check_iterator_arguments(items,"standard",["multistandard","body","collection","class"],kwargs)

        '''
        for std in self.standards.values():
        '''
        # use the following two lines instead, to get the standards sorted
        for s in sorted(self.standards):
            std = self.standards[s]

            its = {"standard" : std}
            its["class"] = self.class_standards.get_src(std)
            its["body"] = self.body_standards.get_src(std)

            if self.multistandard_standards.contains_dst(std):
                its["multistandard"] = self.multistandard_standards.get_src(std)
                its["collection"] = self.collection_multistandards.get_src(its["multistandard"])
            else:
                its["multistandard"] = None
                its["collection"] = self.collection_standards.get_src(std)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def itermultistandards(self,items=["multistandard"],**kwargs):
        """
        Iterator over all multistandards of the repo.

        Possible items to rerquest: multistandard, standards, collection, body
        """
        check_iterator_arguments(items,"multistandard",["standards","collection","body"],kwargs)

        for mstandard in self.multistandards.values():
            its = {"multistandard" : mstandard}
            its["standards"] = self.multistandard_standards.get_dsts(mstandard)
            its["collection"] = self.collection_multistandards.get_src(mstandard)
            its["body"] = self.body_multistandards.get_src(mstandard)

            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def iterclasses(self,items=["class"],**kwargs):
        """
        Iterator over all classes of the repo.

        Possible items to request: class, collection
        """
        check_iterator_arguments(items,"class",["collection"],kwargs)

        for cl in self.classes.values():
            its = {"class" : cl}
            its["collection"] = self.collection_classes.get_src(cl)
            if filter_iterator_items(its,kwargs):
                yield tuple(its[key] for key in items)

    def itercollections(self):
        """
        Iterator over all collections of the repo.

        Not possible to request items
        """
        '''
        for coll in self.collections.values():
            yield (coll,)
        '''
        # use these to get the collections sorted by their names
        for coll in sorted(self.collections):
            yield (self.collections[coll],)

    def iterbodies(self):
        """
        Iterator over all standard bodies of the repo.

        Not possible to request items
        """
        '''
        for body in self.bodies.values():
            yield (body,)
        '''
        # use these to get the bodies sorted by their names
        for body in sorted(self.bodies):
            yield (self.bodies[body],)
