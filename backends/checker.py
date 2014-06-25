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
from os.path import join, exists, basename, splitext
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
			row.append(cl.id in dbs["freecad"].getbase)
			row.append(cl.id in dbs["openscad"].getbase)
			if not (row[-1] and row[-2]):
				self.rows.append(row)

class UnknownClassTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Unknown classes",
			"Some classes are mentioned in base files, but never defined in blt files.",
			["Class id", "Database"]
		)

	def populate(self,repo,dbs):
		for db in ["openscad","freecad"]:
			for base in dbs[db].getbase.values():
				for cl_id in base.classids:
					if cl_id not in repo.classes:
						row = []
						row.append(cl_id)
						row.append(db)
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

class UnknownConnectorLocationTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Unknown locations",
			"Some connector locations are mentioned that are not defined.",
			["Class id", "Locations", "Collection"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			if not cl.id in dbs["openscad"].getbase:
				continue
			#find all locations
			base = dbs["openscad"].getbase[cl.id]
			locations = []
			if base.type == "module" and not base.connectors is None:
				locations = base.connectors.locations

			#collect all locations covered by drawings
			covered = []
			if dbs["drawings"].connectors_classes.contains_dst(cl):
				for con in dbs["drawings"].connectors_classes.get_srcs(cl):
					for loc in dbs["drawings"].locations_connectors.get_srcs(con):
						covered.append(loc)

			unknown = set(covered) - set(locations)
			if len(unknown) > 0:
				row = []
				row.append(cl.id)
				row.append(",".join(list(uncovered)))
				row.append(repo.collection_classes.get_src(cl).name)
				self.rows.append(row)

class MissingConnectorTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing connectors",
			"Some classes have no connectors for OpenSCAD specified.",
			["Class ID","Collection"]
		)

	def populate(self,repo,dbs):
		for cl in repo.classes.values():
			if not cl.id in dbs["openscad"].getbase:
				continue

			base = dbs["openscad"].getbase[cl.id]
			if base.type == "module" and not base.connectors is None:
				continue

			row = []
			row.append(cl.id)
			row.append(repo.collection_classes.get_src(cl).name)
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
			if not cl.id in dbs["openscad"].getbase:
				continue
			#find all locations
			base = dbs["openscad"].getbase[cl.id]
			locations = []
			if base.type == "module" and not base.connectors is None:
				locations = base.connectors.locations

			#collect all locations covered by drawings
			covered = []
			if dbs["drawings"].connectors_classes.contains_dst(cl):
				for con in dbs["drawings"].connectors_classes.get_srcs(cl):
					for loc in dbs["drawings"].locations_connectors.get_srcs(con):
						covered.append(loc)

			uncovered = set(locations) - set(covered)
			if len(uncovered) > 0:
				row = []
				row.append(cl.id)
				row.append("Connectors")
				row.append(",".join(list(uncovered)))
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
			for id, base in dbs[db].getbase.iteritems():
				if not license.check_license(base.license_name,base.license_url):
					row = []
					row.append(db)
					row.append(id)
					row.append(base.license_name)
					row.append(base.license_url)
					row.append(",".join(coll.authors))
					self.rows.append(row)
		#drawings
		for draw in dbs["drawings"].dimensions:
			if not license.check_license(draw.license_name,draw.license_url):
				row = []
				row.append("drawing-dimension")
				row.append(",".join([cl.id for cl in dbs["drawings"].dimension_classes.get_dsts()]))
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
		for db in dbs:
			if db in ["drawings","solidworks"]:
				continue
			for coll in repo.collections.values():
				path = join(repo.path,db,coll.id)
				if not exists(path):
					continue
				files = listdir(path)

				#remove files known from bases
				for cl in repo.collection_classes.get_dsts(coll):
					if not cl.id in dbs[db].getbase:
						continue
					base = dbs[db].getbase[cl.id]
					if base.filename in files:
						files.remove(base.filename)

				#check what is left
				for filename in files:
					if splitext(filename)[1] == ".base":
						continue
					row = []
					row.append(filename)
					row.append(path)
					self.rows.append(row)

		if "drawings" in dbs:
			for coll in repo.collections.values():
				path = join(repo.path,"drawings",coll.id)
				if not exists(path):
					continue

				files = listdir(path)

				#remove files known from bases
				for cl in repo.collection_classes.get_dsts(coll):
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

				#check what is left
				for filename in files:
					if splitext(filename)[1] == ".base":
						continue
					row = []
					row.append(filename)
					row.append(path)
					self.rows.append(row)

		if "solidworks" in dbs:
			for coll in repo.collections.values():
				path = join(repo.path,"solidworks",coll.id)
				if not exists(path):
					continue

				files = listdir(path)

				#remove files known from bases
				for dtable in dbs["solidworks"].designtables:
					if not coll.id == dtable.collection:
						continue
					files.remove(dtable.filename)

				#check what is left
				for filename in files:
					if splitext(filename)[1] == ".base":
						continue
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

class MissingBaseConnectionTable(ErrorTable):
	def __init__(self):
		ErrorTable.__init__(self,
			"Missing Base Connections",
			"There are possibilities to assign classes to base geometries that are not used",
			["Backend","Filename","missing classes"]
		)

	def populate(self,repo,dbs):
		#collect sets of classes with equivalent geometry
		geo_eq = []
		for db in ["freecad","openscad"]:
			for base in dbs[db].getbase.values():
				geo_eq.append(set(base.classids))
		for dtable in dbs["solidworks"].designtables:
			geo_eq.append(set([dtc.classid for dtc in dtable.classes]))

		#consolidate geo equivalent sets TODO: what is that operation called in cs lingo? algos?
		while True:
			geo_cns = []
			for cl in repo.classes.values():
				cn = set([])
				for eq in geo_eq:
					if cl.id in eq:
						cn = cn.union(eq)
				if not cn in geo_cns:
					geo_cns.append(cn)
			if len(geo_cns) == len(geo_eq):
				geo_eq = geo_cns
				break
			geo_eq = geo_cns

		#check whether we are missing something
		for db in ["freecad","openscad"]:
			for base in dbs[db].getbase.values():
				classids = set(base.classids)
				for eq in geo_eq:
					if not classids.isdisjoint(eq) and eq > classids:
						self.rows.append([db,base.filename,str(eq - classids)])
		drawings = dbs["drawings"]
		for draw in drawings.dimensions:
			if not drawings.dimension_classes.contains_src(draw):
				continue
			classids = set([cl.id for cl in drawings.dimension_classes.get_dsts(draw)])
			for eq in geo_eq:
				if not classids.isdisjoint(eq) and eq > classids:
					self.rows.append(["drawings",base.filename,str(eq - classids)])

		for draw in drawings.connectors:
			if not drawings.connectors_classes.contains_src(draw):
				continue
			classids = set([cl.id for cl in drawings.connectors_classes.get_dsts(draw)])
			for eq in geo_eq:
				if not classids.isdisjoint(eq) and eq > classids:
					self.rows.append(["connector",base.filename,str(eq - classids)])


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
		self.checks["unknownclass"] = UnknownClassTable()
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
