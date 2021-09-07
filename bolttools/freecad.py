# Copyright 2012-2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
# Copyright (C) 2021 Bernd Hahnebach <bernd@bimstatik.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .common import BaseStandardFunction
from .common import check_iterator_arguments
from .common import filter_iterator_items
from .common import StandardDataBase


class BaseFunction(BaseStandardFunction):

    def __init__(self, function, basefile, collname, backend_root):
        BaseStandardFunction.__init__(self, function, basefile, collname, backend_root)


class FreeCADData(StandardDataBase):

    def __init__(self, repo):
        StandardDataBase.__init__(self, repo, "freecad", BaseFunction)


    def iterbases(self, items=["base"], **kwargs):
        """
        Iterator over all freecad bases of the repo.

        Possible items to request: base, classes, collection
        """

        # basefiles are used in freecad and allplan backend only

        check_iterator_arguments(items, "base", ["classes", "collection"], kwargs)

        for base in self.bases:
            its = {"base": base}
            its["collection"] = self.collection_bases.get_src(base)
            its["classes"] = self.base_classes.get_dsts(base)

            if filter_iterator_items(its, kwargs):
                yield tuple(its[key] for key in items)


