#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

#common stuff

import re
from os import listdir,makedirs, remove
from os.path import join, exists, isfile
from shutil import rmtree
from copy import deepcopy

class BackendExporter:
	def __init__(self,repo):
		self.repo = repo
	def clear_output_dir(self,out_dir):
		# pylint: disable=R0201
		if not exists(out_dir):
			makedirs(out_dir)
		for path in listdir(out_dir):
			full_path = join(out_dir,path)
			if isfile(full_path):
				remove(full_path)
			else:
				rmtree(full_path)
