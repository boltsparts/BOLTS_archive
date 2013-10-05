#!/usr/bin/env python
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


