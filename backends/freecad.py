# Copyright 2012-2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
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

# pylint: disable=W0622


class FreeCADBackend(Backend):
    def __init__(self, repo, databases):
        Backend.__init__(self, repo, "freecad", databases, ["freecad"])

    def write_output(self, out_path, **kwargs):
        self.args = self.validate_arguments(kwargs, ["target_license", "version"])
        self.license = license

        self.clear_output_dir(out_path)
        self.bout_path = join(out_path, "BOLTS")

        # generate macro
        start_macro = open(join(out_path, "start_bolts.FCMacro"), "w")
        start_macro.write("import BOLTS\n")
        start_macro.write("BOLTS.show_widget()\n")
        start_macro.close()

        # copy files bolttools
        if not self.license.is_combinable_with("LGPL 2.1+", self.args["target_license"]):
            raise IncompatibleLicenseError(
                "bolttools is LGPL 2.1+, which is not compatible with {}"
                .format(self.args["target_license"])
            )
        copytree(
            join(self.repo.path, "bolttools"),
            join(self.bout_path, "bolttools")
        )
        # remove the test suite and documentation, to save space
        rmtree(join(self.bout_path, "bolttools", "test_blt"))

        # generate version file
        date = datetime.now()
        version_file = open(join(self.bout_path, "VERSION"), "w")
        version_file.write(
            "{}\n{}-{}-{}\n{}\n".format(
                self.args["version"],
                date.year,
                date.month,
                date.day,
                self.args["target_license"]
            )
        )
        version_file.close()

        # copy freecad directory in backend
        if not self.license.is_combinable_with("LGPL 2.1+", self.args["target_license"]):
            raise IncompatibleLicenseError(
                "FreeCAD gui files are LGPL 2.1+, "
                "which is not compatible with {}"
                .format(self.args["target_license"])
            )
        if not exists(join(self.bout_path, "freecad")):
            makedirs(join(self.bout_path, "freecad"))
        open(join(self.bout_path, "freecad", "__init__.py"), "w").close()

        copytree(
            join(self.repo.path, "backends", "freecad", "app"),
            join(self.bout_path, "app")
        )
        copytree(
            join(self.repo.path, "backends", "freecad", "gui"),
            join(self.bout_path, "gui")
        )
        copytree(
            join(self.repo.path, "backends", "freecad", "assets"),
            join(self.bout_path, "assets")
        )
        copytree(
            join(self.repo.path, "icons"),
            join(self.bout_path, "icons")
        )
        copyfile(
            join(self.repo.path, "backends", "freecad", "init.py"),
            join(self.bout_path, "__init__.py")
        )
        copyfile(
            join(self.repo.path, "backends", "common", "repo_tools.py"),
            join(self.bout_path, "repo_tools.py")
        )
        open(join(self.bout_path, "gui", "__init__.py"), "w").close()

        # copy data and creator modules
        self.copy_data_and_creator_modules()
