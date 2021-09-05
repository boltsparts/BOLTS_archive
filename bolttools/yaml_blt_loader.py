# bolttools - a framework for creation of part libraries
# Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
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


import yaml

from . import yaml_in_yaml


def load_yaml_blt(file_to_load):

    data = list(yaml.load_all(open(file_to_load), Loader=yaml_in_yaml.Loader))

    return data


# readonly, utf8?

# TODO copy the new separated geometric profile files
# for all distributions


"""
# with open funktioniert nicht ... ?
    with open(file_to_load) as f:

        return list(yaml.load(f, yaml_in_yaml.Loader))
"""
