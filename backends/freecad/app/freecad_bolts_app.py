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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import importlib

from ..bolttools import freecad


# *******
# TODO somehow return the part if added from Python
#********


def add_part(collection, base, params, doc):
    if isinstance(base, freecad.BaseFunction):

        # absolute import BOLTS hardcoded
        # does not work for FreeCAD new style wb
        # module = importlib.import_module("BOLTS.freecad.%s.%s" %
        #     (collection.id,base.module_name))
        # example: import BOLTS.freecad.profile_l.profile_l

        # use relative import
        # example: import ..freecad.profile_l.profile_l

        print("{}".format(collection.id))
        print("{}".format(base.module_name))
        print(params)
        print(doc.Name)
        print(__package__)  # BOLTS.app for old style FreeCAD wb

        module = importlib.import_module(
            ".freecad.{}.{}".format(collection.id, base.module_name),
            package=__package__.rstrip(".app")
        )
        print(module)
        module.__dict__[base.name](params, doc)

    else:
        raise RuntimeError("Unknown base geometry type: %s" % type(base))
