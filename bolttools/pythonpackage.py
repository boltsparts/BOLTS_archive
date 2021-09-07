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

from .common import StandardDataBase


# PythonPackage distribution has no modules to create geometry
# thus no base files at all
# thus no classes for representing the data in the base files needed.


# TODO is this db_repo really needed?
# the base files ar not existent.
# The iterators are available at the repo as well


class PythonPackageData(StandardDataBase):

    def __init__(self, repo):
        StandardDataBase.__init__(self, repo, "pythonpackage")
