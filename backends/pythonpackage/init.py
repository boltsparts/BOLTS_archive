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

from os.path import dirname

from .bolttools import blt
from .bolttools import pythonpackage


# import repo
rootpath = dirname(__file__)
repo = blt.Repository(rootpath)
# print(repo)
db_repo = pythonpackage.PythonPackageData(repo)
