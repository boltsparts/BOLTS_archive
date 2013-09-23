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

#common stuff for the backends

from os import listdir,makedirs, remove
from os.path import join, exists, basename, isfile
from shutil import rmtree,copy

class BackendData:
	def __init__(self,name,path):
		self.repo_root = path
		self.backend_root = join(path,name)
		self.out_root = join(path,"output",name)


class BackendExporter:
	def clear_output_dir(self,backend_data):
		if not exists(backend_data.out_root):
			makedirs(backend_data.out_root)
		for path in listdir(backend_data.out_root):
			full_path = join(backend_data.out_root,path)
			if isfile(full_path):
				remove(full_path)
			else:
				rmtree(full_path)
