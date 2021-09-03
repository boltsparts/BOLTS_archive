# bolttools - a framework for creation of part libraries
# Copyright (C) 2021 Bernd Hahnebach <bernd@bimstatik.org>

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

from codecs import open
from datetime import datetime
from os import makedirs
from os.path import basename
from os.path import exists
from os.path import join
from shutil import copy
from shutil import copyfile
from shutil import copytree
from shutil import rmtree

from . import license
from .common import Backend
from .errors import IncompatibleLicenseError


class PythonPackageBackend(Backend):
    def __init__(self, repo, databases):
        Backend.__init__(self, repo, "pythonpackage", databases, ["pythonpackage"])

    def write_output(self, out_path, **kwargs):
        args = self.validate_arguments(kwargs, ["target_license", "version"])

        self.clear_output_dir(out_path)

        bolts_path = join(out_path, "boltspy")
        makedirs(bolts_path)

        # generate version file
        date = datetime.now()
        with open(join(bolts_path, "VERSION"), "w") as version_file:
            version_file.write("%s\n%d-%d-%d\n%s\n" %
                (args["version"], date.year, date.month, date.day, args["target_license"]))

        # copy bolttools files
        if not license.is_combinable_with("LGPL 2.1+", args["target_license"]):
            raise IncompatibleLicenseError(
                "bolttools is LGPL 2.1+, which is not compatible with %s" % args["target_license"])
        copytree(join(self.repo.path, "bolttools"), join(bolts_path, "bolttools"))
        # remove the test suite and documentation, to save space
        rmtree(join(bolts_path, "bolttools", "test_blt"))

        copyfile(
            join(self.repo.path, "backends", "pythonpackage", "init.py"),
            join(bolts_path, "__init__.py")
        )
        copyfile(
            join(self.repo.path, "backends", "common", "repo_tools.py"),
            join(bolts_path, "repo_tools.py")
        )

        # copy part data
        if not exists(join(bolts_path, "data")):
            makedirs(join(bolts_path, "data"))
        if not exists(join(bolts_path, "pythonpackage")):
            makedirs(join(bolts_path, "pythonpackage"))

        for coll, in self.repo.itercollections():

            # copy all part data
            # skip collection if licenses issues
            if not license.is_combinable_with(coll.license_name, args["target_license"]):
                print("Skip %s due to license issues" % coll.id)
                continue

            copy(
                join(self.repo.path, "data", "%s.blt" % coll.id),
                join(bolts_path, "data", "%s.blt" % coll.id)
            )
