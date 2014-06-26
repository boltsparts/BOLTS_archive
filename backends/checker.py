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

from os import listdir
from os.path import join, exists, basename, splitext, isdir
import re

from common import BackendExporter
import license
from errors import *

class ErrorTable:
	def __init__(self,title,description,headers):
		self.title = title
		self.description = description
		self.rows = []
		self.headers = headers

	def populate(self,repo,databases):
		raise NotImplementedError

	def get_headers(self):
		return self.headers

	def get_title(self):
		return self.title

	def get_description(self):
		return self.description

	def get_table(self):
		return self.rows

	def print_table(self):
		if len(self.rows) == 0:
			return ""

		res = []
		res.append(self.title)
		res.append('-'*len(self.title) + '\n')
		res.append(self.description + '\n')

		#determine maximum field width
		width = []
		for field in self.headers:
			width.append(len(field))
		for row in self.rows:
			for i in range(len(row)):
				width[i] = max(len(str(row[i])),width[i])

		#add some more space
		for i in range(len(width)):
			width[i] += 2

		#print headers
		res.append("".join("%-*s" % (width[i],self.headers[i]) for i in range(len(self.headers))))
		res.append("".join("-"*w for w in width))

		for row in self.rows:
			res.append("".join("%-*s" % (w,v) for w,v in zip(width,row)))
		res.append("\n")
		return "\n".join(res)


class MissingBaseTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing base geometries",
			"Some classes can not be used in one or more CAD packages, because no geometry is available.",
			["Class id","Collection","FreeCAD","OpenSCAD"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			row = []
			row.append(cl.id)
			row.append(repo.collection_classes.get_src(cl).name)
			row.append(dbs["freecad"].base_classes.contains_dst(cl))
			row.append(dbs["openscad"].base_classes.contains_dst(cl))
			if not (row[-1] and row[-2]):
				self.rows.append(row)

class MissingCommonParametersTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing common parameters",
			"Some classes have no common parameters defined.",
			["Class ID","Collection"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			if cl.parameters.common is None:
				row = []
				row.append(cl.id)
				row.append(repo.collection_classes.get_src(cl).name)
				self.rows.append(row)

class MissingConnectorTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing connectors",
			"Some OpenSCAD bases have no connectors specified.",
			["Collection","Class IDs"]
		)

	def populate(self,repo,dbs):
		for base in dbs["openscad"].bases:
			if not dbs["openscad"].base_connectors.contains_src(base):
				row = []
				row.append(dbs["openscad"].collection_bases.get_src(base).name)
				row.append(",".join([cl.id for cl in dbs["openscad"].base_classes.get_dsts(base)]))
				self.rows.append(row)

class MissingDrawingTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing drawings",
			"Some classes do not have associated drawings.",
			["Class id", "Drawing type", "Locations", "Collection"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			#dimension drawings
			if not dbs["drawings"].dimension_classes.contains_dst(cl):
				row = []
				row.append(cl.id)
				row.append("Dimensions")
				row.append("-")
				row.append(repo.collection_classes.get_src(cl).name)
				self.rows.append(row)

			#connector drawings
			if not dbs["openscad"].base_classes.contains_dst(cl):
				#if no OpenSCAD base exists for this class
				continue

			#find all locations
			base = dbs["openscad"].base_classes.get_src(cl)
			if not dbs["openscad"].base_connectors.contains_src(base):
				#if no connector is defined fot this base
				continue
			locations = dbs["openscad"].base_connectors.get_dst(base).locations

			#collect all locations covered by drawings
			covered = []
			if dbs["drawings"].connectors_classes.contains_dst(cl):
				for con in dbs["drawings"].connectors_classes.get_srcs(cl):
					covered += dbs["drawings"].locations_connectors.get_srcs(con)

			uncovered = set(locations) - set(covered)
			if len(uncovered) > 0:
				row = []
				row.append(cl.id)
				row.append("Connectors")
				row.append(",".join(list(uncovered)))
				row.append(repo.collection_classes.get_src(cl).name)
				self.rows.append(row)

class UnknownConnectorLocationTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Unknown locations",
			"Some connector locations are mentioned that are not defined.",
			["Class id", "Locations", "Collection"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			if not dbs["openscad"].base_classes.contains_dst(cl):
				#if no OpenSCAD base exists for this class
				continue

			#find all locations
			base = dbs["openscad"].base_classes.get_src(cl)
			if not dbs["openscad"].base_connectors.contains_src(base):
				#if no connector is defined fot this base
				continue
			locations = dbs["openscad"].base_connectors.get_dst(base).locations

			#collect all locations covered by drawings
			covered = []
			if dbs["drawings"].connectors_classes.contains_dst(cl):
				for con in dbs["drawings"].connectors_classes.get_srcs(cl):
					covered += dbs["drawings"].locations_connectors.get_srcs(con)

			unknown = set(covered) - set(locations)
			if len(unknown) > 0:
				row = []
				row.append(cl.id)
				row.append(",".join(list(unknown)))
				row.append(repo.collection_classes.get_src(cl).name)
				self.rows.append(row)


class MissingSVGSourceTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing svg drawings",
			"Some drawings have no svg version.",
			["Collection", "Filename"]
		)

	def populate(self,repo,dbs):
		#connector drawings come without svg source, so dimensions only
		for draw in dbs["drawings"].dimensions:
			if draw.get_svg() is None:
				row = []
				coll = dbs["drawings"].collection_dimensions.get_src(draw)
				row.append(coll.name)
				row.append(draw.filename)
				self.rows.append(row)

class UnsupportedLicenseTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Incompatible Licenses",
			"Some collections or base geometries have unknown licenses.",
			["Type","Id/Filename","License name","License url", "Authors"]
		)

	def populate(self,repo,dbs):
		#collections
		for coll in repo.collections.values():
			if not license.check_license(coll.license_name,coll.license_url):
				row = []
				row.append("Collection")
				row.append(coll.id)
				row.append(coll.license_name)
				row.append(coll.license_url)
				row.append(",".join(coll.authors))
				self.rows.append(row)
		#bases
		for db in ["openscad","freecad"]:
			for base in dbs[db].bases:
				if not license.check_license(base.license_name,base.license_url):
					row = []
					row.append(db)
					row.append(",".join([cl.id for cl in dbs[db].base_classes.get_dsts(id)]))
					row.append(base.license_name)
					row.append(base.license_url)
					row.append(",".join(coll.authors))
					self.rows.append(row)
		#drawings
		for draw in dbs["drawings"].dimensions:
			if not license.check_license(draw.license_name,draw.license_url):
				row = []
				row.append("drawing-dimension")
				row.append(",".join([cl.id for cl in dbs["drawings"].dimension_classes.get_dsts(draw)]))
				row.append(draw.license_name)
				row.append(draw.license_url)
				row.append(",".join(coll.authors))
				self.rows.append(row)
		for draw in dbs["drawings"].connectors:
			if not license.check_license(draw.license_name,draw.license_url):
				row = []
				row.append("drawing-connector")
				row.append(",".join([cl.id for cl in dbs["drawings"].connector_classes.get_dsts()]))
				row.append(draw.license_name)
				row.append(draw.license_url)
				row.append(",".join(coll.authors))
				self.rows.append(row)

class UnknownFileTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Stray files",
			"Some files are present in the repository, but not mentioned anywhere.",
			["Filename","Path"]
		)

	def populate(self,repo,dbs):
		if "freecad" in dbs:
			for collid in listdir(join(repo.path,"freecad")):
				path = join(repo.path,"freecad",collid)
				if isdir(path):
					files = listdir(path)
				else:
					files = [collid]

				if collid in repo.collections:
					if "%s.base" % collid in files:
						files.remove("%s.base" % collid)
						for cl in repo.collection_classes.get_dsts(repo.collections[collid]):
							if not dbs["freecad"].base_classes.contains_dst(cl):
								continue
							base = dbs["freecad"].base_classes.get_src(cl)
							if base.filename in files:
								files.remove(base.filename)

				for filename in files:
					row = []
					row.append(filename)
					row.append(path)
					self.rows.append(row)

		if "openscad" in dbs:
			for collid in listdir(join(repo.path,"openscad")):
				path = join(repo.path,"openscad",collid)
				if isdir(path):
					files = listdir(path)
				else:
					files = [path]

				if collid in repo.collections:
					if "%s.base" % collid in files:
						files.remove("%s.base" % collid)
						for cl in repo.collection_classes.get_dsts(repo.collections[collid]):
							if not dbs["openscad"].base_classes.contains_dst(cl):
								continue
							base = dbs["openscad"].base_classes.get_src(cl)
							if base.filename in files:
								files.remove(base.filename)

				for filename in files:
					row = []
					row.append(filename)
					row.append(path)
					self.rows.append(row)

#			if "solidworks" in dbs:
#				files = []
#				path = join(repo.path,"solidworks",coll.id)
#				if exists(path):
#					files = listdir(path)
#
#				if "%s.base" % coll.id in files:
#					files.remove("%s.base" % coll.id)
#				for dtable in dbs["solidworks"].designtables:
#					if not coll.id == dtable.collection:
#						continue
#					files.remove(dtable.filename)
#
#				for filename in files:
#					row = []
#					row.append(filename)
#					row.append(path)
#					self.rows.append(row)

		if "drawings" in dbs:
			for collid in listdir(join(repo.path,"drawings")):
				path = join(repo.path,"drawings",collid)
				if isdir(path):
					files = listdir(path)
				else:
					files = [collid]

				if collid in repo.collections:
					if "%s.base" % collid in files:
						files.remove("%s.base" % collid)
						for cl in repo.collection_classes.get_dsts(repo.collections[collid]):
							drawings = []
							if dbs["drawings"].dimension_classes.contains_dst(cl):
								drawings.append(dbs["drawings"].dimension_classes.get_src(cl))
							if dbs["drawings"].connectors_classes.contains_dst(cl):
								drawings += dbs["drawings"].connectors_classes.get_srcs(cl)
							for draw in drawings:
								if not draw.get_png() is None:
									if basename(draw.get_png()) in files:
										files.remove(basename(draw.get_png()))
								if not draw.get_svg() is None:
									if basename(draw.get_svg()) in files:
										files.remove(basename(draw.get_svg()))

			for filename in files:
				row = []
				row.append(filename)
				row.append(path)
				self.rows.append(row)

class NonconformingParameternameTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Nonconforming Parameter names",
			"Parameter names should start with a upper- or lowercase letter. The rest of the name should consist of only lowercase letters, numbers and underscores",
			["Parameter name","Class id","Collection"]
		)

	def populate(self,repo,dbs):
		schema = re.compile("[a-zA-z][a-z0-9_]*")
		for cl in repo.classes.values():
			for pname in cl.parameters.parameters:
				match = schema.match(pname)
				if match is None or (not match.group(0) == pname):
					row = []
					row.append(pname)
					row.append(cl.id)
					row.append(repo.collection_classes.get_src(cl).name)
					self.rows.append(row)



class HyperUnionFind:
	"""
	Naive implementation of a disjoint set or union find datastructure for
	hypergraphs
	"""
	def __init__(self):
		self.components = {}
	def make_set(self,x):
		for comp in self.components.values():
			assert(not x in comp)
		self.components[x] = set([x])
	def find_set(self,x):
		for c,comp in self.components.iteritems():
			if x in comp:
				return c
		raise ValueError("Unknown element: %s" % x)
	def union(self,x,y):
		rx = self.find_set(x)
		ry = self.find_set(y)
		self.components[rx] |= self.components[ry]
		del self.components[ry]
	def process_edge(self,e):
		rep = None
		for v in e:
			if rep is None:
				rep = v
			else:
				if self.find_set(rep) != self.find_set(v):
					self.union(rep,v)
	def get_set(self,x):
		return self.components[self.find_set(x)]

class MissingBaseConnectionTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing Base Connections",
			"There are possibilities to assign classes to base geometries that are not used",
			["Backend","Filename","missing classes"]
		)

	def populate(self,repo,dbs):
		#collect sets of classes with equivalent geometry
		union = HyperUnionFind()
		for cl in repo.classes.values():
			union.make_set(cl.id)
		#find connected components of the hypergraph formed by the equivalent geometry relations
		for base in dbs["freecad"].bases:
			union.process_edge(set(base.classids))
		for base in dbs["openscad"].bases:
			union.process_edge(set(base.classids))
		for dtable in dbs["solidworks"].designtables:
			union.process_edge(set([dtc.classid for dtc in dtable.classes]))

		#check whether we are missing something
		for db in ["freecad","openscad"]:
			for base in dbs[db].bases:
				eq = union.get_set(base.classids[0])
				classids = set(base.classids)
				if  eq > classids:
					self.rows.append([db,base.filename,",".join(eq - classids)])

		drawings = dbs["drawings"]

		for draw in drawings.dimensions:
			classids = set([cl.id for cl in drawings.dimension_classes.get_dsts(draw)])
			eq = union.get_set(drawings.dimension_classes.get_dsts(draw)[0].id)
			if  eq > classids:
				self.rows.append(["Dimension drawing",draw.filename,",".join(eq - classids)])

		for draw in drawings.connectors:
			classids = set([cl.id for cl in drawings.connectors_classes.get_dsts(draw)])
			eq = union.get_set(drawings.connectors_classes.get_dsts(draw)[0].id)
			if  eq > classids:
				self.rows.append(["Connector drawing",draw.filename,",".join(eq - classids)])

class MissingParameterDescriptionTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing parameter description",
			"Some classes have no human readable description of their parameters.",
			["Class id","Collection","parameters"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			row = []
			row.append(cl.id)
			row.append(repo.collection_classes.get_src(cl).name)

			missing = []
			for pname in cl.parameters.parameters:
				if not pname in cl.parameters.description:
					missing.append(pname)

			if len(missing) > 0:
				row.append(', '.join(missing))
				self.rows.append(row)


class CheckerExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)

		self.checks = {}
		self.checks["unsupportedlicense"] = UnsupportedLicenseTable()
		self.checks["unknownfile"] = UnknownFileTable()
		self.checks["nonconformingparametername"] = NonconformingParameternameTable()
		self.checks["missingbaseconnection"] = MissingBaseConnectionTable()
		self.checks["missingparameterdescription"] = MissingParameterDescriptionTable()
		self.checks["unknownconnectors"] = UnknownConnectorLocationTable()

		self.tasks = {}
		self.tasks["missingcommonparameters"] = MissingCommonParametersTable()
		self.tasks["missingconnectors"] = MissingConnectorTable()
		self.tasks["missingbase"] = MissingBaseTable()
		self.tasks["missingdrawing"] = MissingDrawingTable()
		self.tasks["missingsvgsource"] = MissingSVGSourceTable()

		for check in self.checks.values():
			check.populate(repo,databases)

		for task in self.tasks.values():
			task.populate(repo,databases)

	def write_output(self,out_path):
		pass
