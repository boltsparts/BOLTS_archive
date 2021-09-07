# bolttools - a framework for creation of part libraries
# Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
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

# common stuff

from os import listdir
from os import makedirs
from os import remove
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import isfile
from os.path import join
from shutil import copy
from shutil import copyfile
from shutil import copytree
from shutil import rmtree
from .errors import DatabaseNotAvailableError
from .errors import UnknownArgumentError


UNITS = {"Length (mm)": "mm", "Length (in)": "in"}


class Backend:
    """
    Base class for backends.

    takes care of validating and storing databases, clearing the output directory
    """
    def __init__(self, repo, name, databases, required=[], optional={}):
        """
        required and optional are list of strings for databases that
        are required or optional for the correct function of this
        backend
        """
        self.repo = repo
        self.name = name
        self.dbs = {}
        for db in required:
            if db not in databases:
                raise DatabaseNotAvailableError(self.name, db)
            self.dbs[db] = databases[db]
        for db in optional:
            if db in databases:
                self.dbs[db] = databases[db]

    def clear_output_dir(self, out_dir):
        if not exists(out_dir):
            makedirs(out_dir)
        for path in listdir(out_dir):
            full_path = join(out_dir, path)
            if isfile(full_path):
                remove(full_path)
            else:
                rmtree(full_path)

    def validate_arguments(self, kwargs, required=[], optional={}):
        """
        normalises and validates key-value arguments
        kwargs is a dictionary
        required is a list of keys that must be present
        optional is a dict of optional keys, with their default value
        args in kwargs that are not either required or optional are an error conditions
        """
        res = {}
        res.update(optional)
        for key in kwargs:
            if key in required:
                res[key] = kwargs[key]
            elif key in optional:
                res[key] = kwargs[key]
            else:
                raise UnknownArgumentError(self.name, key)
        return res

    def write_ouput(self, out_path, **kwargs):
        raise NotImplementedError()

    def copy_data_and_creator_modules(self, all_data=False):

        if not exists(join(self.bout_path, "data")):
            makedirs(join(self.bout_path, "data"))

        for coll, in self.repo.itercollections():

            # skip if license does not fit
            if (
                not self.license.is_combinable_with(
                    coll.license_name,
                    self.args["target_license"]
                )
            ):
                continue

            # continue if all_data is False and no geometry creator modules exists
            if (
                all_data is False
                and not exists(join(self.repo.path, self.name, coll.id, "%s.base" % coll.id))
            ):
                # print("Skip %s due to missing base file" % coll.id)
                continue

            # copy data structure files
            copy(
                join(self.repo.path, "data", "%s.blt" % coll.id),
                join(self.bout_path, "data", "%s.blt" % coll.id)
            )

            # geoemtry data files
            if isdir(join(self.repo.path, "data", "%s" % coll.id)):
                copytree(
                    join(self.repo.path, "data", "%s" % coll.id),
                    join(self.bout_path, "data", "%s" % coll.id)
                )

            # copy geometry creation files
            # ATM the backend directory has to be created even if it is empty
            # like for the PythonPackage distribution
            if not exists(join(self.bout_path, self.name, coll.id)):
                makedirs(join(self.bout_path, self.name, coll.id))

            # if all data is copied no geometry creator modules are copied
            if all_data is True:
                continue

            if (
                not exists(join(
                    self.repo.path,
                    self.name,
                    coll.id,
                    "%s.base" % coll.id
                ))
            ):
                continue

            copy(
                join(self.repo.path, self.name, coll.id, "%s.base" % coll.id),
                join(self.bout_path, self.name, coll.id, "%s.base" % coll.id)
            )

            open(join(self.bout_path, self.name, coll.id, "__init__.py"), "w").close()

            for base, in self.dbs[self.name].iterbases(filter_collection=coll):
                if base.license_name not in self.license.LICENSES:
                    continue
                if (
                    not self.license.is_combinable_with(
                        base.license_name, self.args["target_license"]
                    )
                ):
                    continue
                copy(
                    join(self.repo.path, self.name, coll.id, basename(base.filename)),
                    join(self.bout_path, self.name, coll.id, basename(base.filename))
                )
