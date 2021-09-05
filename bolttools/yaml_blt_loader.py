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


def load_yaml_blt(basefilename):
    try:
        base = list(yaml.load_all(open(basefilename), Loader=yaml.SafeLoader))
        # SafeLoader is not implemented in pyyaml < 5.1
    except AttributeError:
        # this is deprecated for newer pyyaml versions
        base = list(yaml.load_all(open(basefilename)))
    """
    try:
        base = list(yaml.load_all(open(basefilename,"r","utf8"), Loader=yaml.SafeLoader))
        # SafeLoader is not implemented in pyyaml < 5.1
    except AttributeError:
        # this is deprecated for newer pyyaml versions
        base = list(yaml.load_all(open(basefilename,"r","utf8")))
    """
    return base
