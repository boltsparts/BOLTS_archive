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
from os.path import join
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
        self.args = self.validate_arguments(kwargs, ["target_license", "version"])
        self.license = license

        self.clear_output_dir(out_path)

        self.bout_path = join(out_path, "boltspy")
        makedirs(self.bout_path)

        # generate version file
        date = datetime.now()
        with open(join(self.bout_path, "VERSION"), "w") as version_file:
            version_file.write(
                "%s\n%d-%d-%d\n%s\n"
                % (
                    self.args["version"],
                    date.year,
                    date.month,
                    date.day,
                    self.args["target_license"]
                )
            )

        # copy bolttools files
        if not self.license.is_combinable_with("LGPL 2.1+", self.args["target_license"]):
            raise IncompatibleLicenseError(
                "bolttools is LGPL 2.1+, which is not compatible with %s"
                % self.args["target_license"]
            )
        copytree(join(self.repo.path, "bolttools"), join(self.bout_path, "bolttools"))
        # remove the test suite and documentation, to save space
        rmtree(join(self.bout_path, "bolttools", "test_blt"))

        copyfile(
            join(self.repo.path, "backends", "pythonpackage", "init.py"),
            join(self.bout_path, "__init__.py")
        )
        copyfile(
            join(self.repo.path, "backends", "common", "repo_tools.py"),
            join(self.bout_path, "repo_tools.py")
        )
        copyfile(
            join(self.repo.path, "backends", "common", "README.md"),
            join(self.bout_path, "README.md")
        )

        # copy data and creator modules
        self.copy_data_and_creator_modules(all_data=True)
