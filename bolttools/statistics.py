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

class Statistics:
    def __init__(self,repo,databases):
        self.repo = repo
        self.dbs = databases

        self.stats = {}

        self.stats["classes"] = sum(1 for _ in self.repo.iterclasses())
        self.stats["classes_freecad"] = sum(1 for _ in self.dbs["freecad"].iterclasses())
        self.stats["classes_openscad"] = sum(1 for _ in self.dbs["openscad"].iterclasses())
        self.stats["collections"] = sum(1 for _ in self.repo.itercollections())
        self.stats["standards"] = sum(1 for _ in self.repo.iterstandards())
        self.stats["names"] = sum(1 for _ in self.repo.iternames())
        self.stats["bodies"] = sum(1 for _ in self.repo.iterbodies())

        self.contributors_names = set([])
        for coll, in self.repo.itercollections():
            for name in coll.author_names:
                self.contributors_names.add(name)
        for base, in self.dbs["freecad"].iterbases():
            for name in base.author_names:
                self.contributors_names.add(name)
        for module, in self.dbs["openscad"].itermodules():
            for name in module.author_names:
                self.contributors_names.add(name)
        for draw, in self.dbs["drawings"].iterdimdrawings():
            for name in base.author_names:
                self.contributors_names.add(name)
        for draw, in self.dbs["drawings"].itercondrawings():
            for name in base.author_names:
                self.contributors_names.add(name)
        self.contributors_names = list(self.contributors_names)

        self.stats["contributors"] = len(self.contributors_names)

    def get_statistics(self):
        return self.stats

    def get_contributors(self):
        return self.contributors_names
