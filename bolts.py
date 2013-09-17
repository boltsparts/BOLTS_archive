#!/usr/bin/env python
from bolttools import blt_parser, openscad, freecad
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
		openscad.FreeCADExporter().write_output(repo)


