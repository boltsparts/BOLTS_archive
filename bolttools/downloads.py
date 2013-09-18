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

from os import listdir,makedirs
from os.path import join, exists, basename
from shutil import rmtree,copy, make_archive
from subprocess import Popen, PIPE
from datetime import datetime


#from http://stackoverflow.com/a/12827065
def get_hash():
	gitproc = Popen(['git', 'show-ref'], stdout = PIPE)
	(stdout, stderr) = gitproc.communicate()

	for row in stdout.split('\n'):
		if row.find('HEAD') != -1:
			hash = row.split()[0]
			break

	return hash


class DownloadsData:
	def __init__(self,path):
		self.hash = get_hash()
		self.date = datetime.now().strftime("%Y%m%d")

		self.template = "BOLTS_%s_%s_%s" % ("%s",self.date,self.hash[:6])
		pass

class DownloadsExporter:
	def write_output(self,repo):
		downloads = repo.downloads
		out_path = join(repo.path,"output","downloads")

		if not repo.freecad is None:
			base_name = join(out_path,downloads.template % "freecad")
			root_dir = join(repo.path,"output","freecad")
			print make_archive(base_name,"gztar",root_dir)
			print make_archive(base_name,"zip",root_dir)

		if not repo.openscad is None:
			base_name = join(out_path,downloads.template % "openscad")
			root_dir = join(repo.path,"output","openscad")
			print make_archive(base_name,"gztar",root_dir)
			print make_archive(base_name,"zip",root_dir)

		if not repo.html is None:
			base_name = join(out_path,downloads.template % "html")
			root_dir = join(repo.path,"output","html")
			print make_archive(base_name,"gztar",root_dir)
			print make_archive(base_name,"zip",root_dir)
