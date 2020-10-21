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

from PyQt5 import uic

from . import license
from .common import Backend
from .errors import IncompatibleLicenseError

# pylint: disable=W0622


class FreeCADBackend(Backend):
    def __init__(self, repo, databases):
        Backend.__init__(self, repo, "freecad", databases, ["freecad"])

    def write_output(self, out_path, **kwargs):
        args = self.validate_arguments(kwargs, ["target_license", "version"])

        self.clear_output_dir(out_path)
        bolts_path = join(out_path, "BOLTS")

        # generate macro
        start_macro = open(join(out_path, "start_bolts.FCMacro"), "w")
        start_macro.write("import BOLTS\n")
        start_macro.write("BOLTS.show_widget()\n")
        start_macro.close()

        # copy files
        # bolttools
        if not license.is_combinable_with("LGPL 2.1+", args["target_license"]):
            raise IncompatibleLicenseError(
                "bolttools is LGPL 2.1+, which is not compatible with {}"
                .format(args["target_license"])
            )
        copytree(
            join(
                self.repo.path, "bolttools"
            ),
            join(
                bolts_path, "bolttools"
            )
        )
        # remove the test suite and documentation, to save space
        rmtree(join(bolts_path, "bolttools", "test_blt"))

        # generate version file
        date = datetime.now()
        version_file = open(join(bolts_path, "VERSION"), "w")
        version_file.write(
            "{}\n{}-{}-{}\n{}\n".format(
                args["version"],
                date.year,
                date.month,
                date.day,
                args["target_license"]
            )
        )
        version_file.close()

        # freecad gui code
        if not license.is_combinable_with("LGPL 2.1+", args["target_license"]):
            raise IncompatibleLicenseError(
                "FreeCAD gui files are LGPL 2.1+, "
                "which is not compatible with {}"
                .format(args["target_license"])
            )
        if not exists(join(bolts_path, "freecad")):
            makedirs(join(bolts_path, "freecad"))
        if not exists(join(bolts_path, "data")):
            makedirs(join(bolts_path, "data"))
        open(join(bolts_path, "freecad", "__init__.py"), "w").close()

        copytree(
            join(
                self.repo.path, "backends", "freecad", "gui"
            ),
            join(
                bolts_path, "gui"
            )
        )
        copytree(
            join(
                self.repo.path, "backends", "freecad", "assets"
            ),
            join(
                bolts_path, "assets"
            )
        )
        copytree(
            join(
                self.repo.path, "icons"
            ),
            join(
                bolts_path, "icons"
            )
        )
        copyfile(
            join(
                self.repo.path, "backends", "freecad", "init.py"
            ),
            join(
                bolts_path, "__init__.py"
            )
        )
        open(join(bolts_path, "gui", "__init__.py"), "w").close()

        # compile ui files
        uic.compileUiDir(join(bolts_path, "gui"))

        for coll, in self.repo.itercollections():
            if (
                not license.is_combinable_with(
                    coll.license_name,
                    args["target_license"]
                )
            ):
                continue
            copy(
                join(
                    self.repo.path, "data", "%s.blt" % coll.id
                ),
                join(
                    bolts_path, "data", "%s.blt" % coll.id
                )
            )

            if not exists(join(bolts_path, "freecad", coll.id)):
                makedirs(join(bolts_path, "freecad", coll.id))

            if (
                not exists(join(
                    self.repo.path,
                    "freecad",
                    coll.id,
                    "%s.base" % coll.id
                ))
            ):
                continue

            copy(
                join(
                    self.repo.path, "freecad", coll.id, "%s.base" % coll.id
                ),
                join(
                    bolts_path, "freecad", coll.id, "%s.base" % coll.id
                )
            )

            open(join(
                bolts_path, "freecad", coll.id, "__init__.py"
            ), "w").close()

            for base, in self.dbs["freecad"].iterbases(filter_collection=coll):
                if base.license_name not in license.LICENSES:
                    continue
                if (
                    not license.is_combinable_with(
                        base.license_name, args["target_license"]
                    )
                ):
                    continue
                copy(
                    join(
                        self.repo.path,
                        "freecad",
                        coll.id,
                        basename(base.filename)
                    ),
                    join(
                        bolts_path, "freecad", coll.id, basename(base.filename)
                    )
                )
