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

from common import BackendExporter
import license
from errors import *

class CheckerExporter(BackendExporter):
	def __init__(self,repo,freecad,openscad,drawings):
		BackendExporter.__init__(self,repo)
		self.freecad = freecad
		self.openscad = openscad
		self.drawings = drawings

	def write_output(self,out_path):
		pass

	#classes for which no base geometries are available
	def get_missing_base_table(self):
		rows = []
		for coll in self.repo.collections:
			for cl in coll.classes_by_ids():
				row = {}
				row["class"] = cl
				row["freecad"] = cl.id in self.freecad.getbase
				row["openscad"] = cl.id in self.openscad.getbase
				row["collection"] = coll.id
				if not (row["freecad"] and row["openscad"]):
					rows.append(row)
		return rows


	#classes which are mentioned, but not defined
	def get_unknown_classes_table(self):
		rows = []
		ids = []
		for coll in self.repo.collections:
			for cl in coll.classes_by_ids():
				ids.append(cl.id)

		for base in self.freecad.getbase.values():
			for id in base.classids:
				if id not in ids:
					row = {}
					row["id"] = id
					row["database"] = "FreeCAD"
					rows.append(row)

		for base in self.openscad.getbase.values():
			for id in base.classids:
				if id not in ids:
					row = {}
					row["id"] = id
					row["database"] = "OpenSCAD"
					rows.append(row)

		for base in self.drawings.getbase.values():
			for id in base.classids:
				if id not in ids:
					row = {}
					row["id"] = id
					row["database"] = "Drawings"
					rows.append(row)
		return rows


	#classes with no common parameters
	def get_missing_common_parameters_table(self):
		rows = []
		for coll in self.repo.collections:
			for cl in coll.classes_by_ids():
				if len(cl.parameters.common) == 0:
					row = {}
					row["class"] = cl
					row["collection"] = coll.id
					rows.append(row)
		return rows

	#classes without drawings
	def get_missing_drawings_table(self):
		rows = []
		for coll in self.repo.collections:
			for cl in coll.classes_by_ids():
				if not cl.id in self.drawings.getbase:
					row = {}
					row["class"] = cl
					row["collection"] = coll.id
					rows.append(row)
		return rows

	#drawings without svg  version
	def get_missing_svg_drawings_table(self):
		rows = []
		for id,draw in self.drawings.getbase.iteritems():
			if draw.get_svg() is None:
				row = {}
				row["id"] = id
				row["drawing"] = draw
				rows.append(row)
		return rows

	#collections with unsupported licenses
	def get_unsupported_coll_license_table(self):
		rows = []
		for coll in self.repo.collections:
			if not license.check_license(coll.license_name,coll.license_url):
				row = {}
				row["id"] = coll.id
				row["license_name"] = coll.license_name
				row["license_url"] = coll.license_url
				row["author_names"] = coll.author_names
				row["author_mails"] = coll.author_mails
				rows.append(row)
		return rows

	#bases with unsupported licenses
	def get_unsupported_base_license_table(self):
		rows = []
		for id, base in self.freecad.getbase.iteritems():
			if not license.check_license(base.license_name,base.license_url):
				row = {}
				row["id"] = id
				row["database"] = "FreeCAD"
				row["license_name"] = base.license_name
				row["license_url"] = base.license_url
				row["author_names"] = base.author_names
				row["author_mails"] = base.author_mails
				rows.append(row)

		for id, base in self.openscad.getbase.iteritems():
			if not license.check_license(base.license_name,base.license_url):
				row = {}
				row["id"] = id
				row["database"] = "OpenSCAD"
				row["license_name"] = base.license_name
				row["license_url"] = base.license_url
				row["author_names"] = base.author_names
				row["author_mails"] = base.author_mails
				rows.append(row)

		for id, base in self.drawings.getbase.iteritems():
			if not license.check_license(base.license_name,base.license_url):
				row = {}
				row["id"] = id
				row["database"] = "Drawings"
				row["license_name"] = base.license_name
				row["license_url"] = base.license_url
				row["author_names"] = base.author_names
				row["author_mails"] = base.author_mails
				rows.append(row)
		return rows

	#files that are present, but nowhere mentioned
	def get_stray_files_table(self):
		rows = []
		for coll in self.repo.collections:
			path = join(self.repo.path,"freecad",coll.id)
			if not exists(path):
				continue
			files = listdir(path)

			#remove files known from bases
			for cl in coll.classes_by_ids():
				if not cl.id in self.freecad.getbase:
					continue
				base = self.freecad.getbase[cl.id]
				if base.filename in files:
					files.remove(base.filename)

			#check what is left
			for filename in files:
				if splitext(filename)[1] == ".base":
					continue
				row = {}
				row["filename"] = filename
				row["collection"] = coll.id
				row["path"] = path
				rows.append(row)

		for coll in self.repo.collections:
			path = join(self.repo.path,"openscad",coll.id)
			if not exists(path):
				continue
			files = listdir(path)

			#remove files known from bases
			for cl in coll.classes_by_ids():
				if not cl.id in self.openscad.getbase:
					continue
				base = self.openscad.getbase[cl.id]
				if base.filename in files:
					files.remove(base.filename)

			#check what is left
			for filename in files:
				if splitext(filename)[1] == ".base":
					continue
				row = {}
				row["filename"] = filename
				row["collection"] = coll.id
				row["path"] = path
				rows.append(row)

		for coll in self.repo.collections:
			path = join(self.repo.path,"drawings",coll.id)
			if not exists(path):
				continue
			files = listdir(path)

			#remove files known from bases
			for cl in coll.classes_by_ids():
				if not cl.id in self.drawings.getbase:
					continue
				drawing = self.drawings.getbase[cl.id]
				if not drawing.get_png() is None:
					if basename(drawing.get_png()) in files:
						files.remove(basename(drawing.get_png()))
				if not drawing.get_svg() is None:
					if basename(drawing.get_svg()) in files:
						files.remove(basename(drawing.get_svg()))

			#check what is left
			for filename in files:
				if splitext(filename)[1] == ".base":
					continue
				row = {}
				row["filename"] = filename
				row["collection"] = coll.id
				row["path"] = path
				rows.append(row)
		return rows








	
