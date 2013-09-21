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

from common import BackendData, BackendExporter
from os import listdir,makedirs
from os.path import join, exists, basename
from shutil import rmtree,copy, make_archive
from subprocess import Popen, PIPE, call
from datetime import datetime
import string

class UncommitedChangesError(Exception):
	def __str__(self):
		return "There are uncommited changes in the git repo"

def uncommited_changes_present():
	return call(["git","diff","--exit-code","--quiet"]) == 1


class DownloadsData(BackendData):
	def __init__(self,path):
		BackendData.__init__(self,"downloads",path)

		#find most current release
		self.current = {}
		self.freecad_down = join(self.out_root,"downloads","freecad")
		for filename in sorted(listdir(self.freecad_down)):
			if filename.endswith(".tar.gz"):
				self.current["freecaddevtar"] = filename
			elif filename.endswith(".zip"):
				self.current["freecaddevzip"] = filename

		self.openscad_down = join(self.out_root,"downloads","openscad")
		for filename in sorted(listdir(self.openscad_down)):
			if filename.endswith(".tar.gz"):
				self.current["openscaddevtar"] = filename
			elif filename.endswith(".zip"):
				self.current["openscaddevzip"] = filename

class DownloadsExporter(BackendExporter):
	def write_output(self,repo):
		downloads = repo.downloads
		out_path = downloads.out_root

		#check that there are no uncommited changes
		if uncommited_changes_present():
			raise UncommitedChangesError()

		#construct filename from date and hash
		date = datetime.now().strftime("%Y%m%d%H%M")
		template = "BOLTS_%s_%s" % ("%s",date)

		#create archives
		root_dir = join(repo.path,"output","freecad")
		if (not repo.freecad is None) and exists(root_dir):
			base_name = join(out_path,"downloads","freecad",template % "FreeCAD")
			downloads.current["freecaddevtar"] = basename(make_archive(base_name,"gztar",root_dir))
			downloads.current["freecaddevzip"] = basename(make_archive(base_name,"zip",root_dir))

		root_dir = join(repo.path,"output","openscad")
		if (not repo.openscad is None) and exists(root_dir):
			base_name = join(out_path,"downloads","openscad",template % "OpenSCAD")
			downloads.current["openscaddevtar"] = basename(make_archive(base_name,"gztar",root_dir))
			downloads.current["openscaddevzip"] = basename(make_archive(base_name,"zip",root_dir))

		#generate html page
		template_name = join(downloads.backend_root,"template","downloads.html")
		template = string.Template(open(template_name).read())
		fid = open(join(out_path,"downloads.html"),"w")
		fid.write(template.substitute(downloads.current))
		fid.close()


#		I do not like the fact that I am shipping unprocessed and unstyled html
#		here, but I do not see a nice workflow for processing and styling, so I
#		don't
#		if not repo.html is None:
#			base_name = join(out_path,downloads.template % "html")
#			root_dir = join(repo.path,"output","html")
#			print make_archive(base_name,"gztar",root_dir)
#			print make_archive(base_name,"zip",root_dir)
