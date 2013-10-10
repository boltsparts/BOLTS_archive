#!/usr/bin/env python
#BOLTS - Open Library of Technical Specifications
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

from bolttools import blt_parser, openscad, freecad, html, downloads
from sys import argv, exit
from os import getcwd

if len(argv) < 2:
	print "bolts.py <command>"
	exit(2)

repo = blt_parser.BOLTSRepository(getcwd())

if argv[1] == "export":
	if argv[2] == "openscad" and (not repo.openscad is None):
		openscad.OpenSCADExporter().write_output(repo)
	elif argv[2] == "freecad" and (not repo.freecad is None):
		freecad.FreeCADExporter().write_output(repo)
	elif argv[2] == "html" and (not repo.html is None):
		html.HTMLExporter().write_output(repo)
	elif argv[2] == "downloads" and (not repo.downloads is None):
		downloads.DownloadsExporter().write_output(repo)
	else:
		print "unknown export target: %s" % argv[2]
else:
	print "unknown command: %s" % argv[1]


