# Copyright 2012-2019 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
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

import os
from os import getcwd,walk,listdir
from os.path import join, exists, basename

from .common import Backend
from .website import app
import sys
from flask_frozen import Freezer

class WebsiteBackend(Backend):
	def __init__(self, repo, databases):
		Backend.__init__(self, repo, "website", databases, ["freecad", "openscad", "drawings"])

	def write_output(self, out_path, **kwargs):
		self.clear_output_dir(out_path)
		extra_files = []
		blog_path = os.path.join(self.repo.path,"backends", "website","blog","posts")
		for filename in listdir(blog_path):
			if filename.startswith('.'):
				continue
			extra_files.append(os.path.join(blog_path,filename))

		doc_path = os.path.join(self.repo.path,"backends", "website","docs","sources")
		for dirpath,_,filenames in walk(doc_path):
			for filename in filenames:
				if filename.startswith('.'):
					continue
				extra_files.append(os.path.join(dirpath,filename))

		trans_path = os.path.join(self.repo.path,"translations")
		for dirpath,_,filenames in walk(trans_path):
			for filename in filenames:
				if filename.endswith('.mo'):
					extra_files.append(os.path.join(dirpath,filename))

		#templates
		for dirpath,_,filenames in walk(self.repo.path):
			if os.path.basename(dirpath) == "templates":
				for filename in filenames:
					extra_files.append(os.path.join(dirpath,filename))

		app.config["FREEZER_DESTINATION"] = out_path
		app.config["FREEZER_BASE_URL"] = "https://boltsparts.github.io"
		app.config["FREEZER_DESTINATION_IGNORE"] = [".git*"]
		app.config["FREEZER_STATIC_IGNORE"] = ["source/*"]

		freezer = Freezer(app)
		freezer.freeze()
