from bolttools import blt_parser, openscad, freecad
from sys import argv

repo = blt_parser.BOLTSRepository(".")

if argv[1] == "export":
	if argv[2] == "openscad" and (not repo.openscad is None):
		openscad.OpenSCADExporter().write_output(repo)
	elif argv[2] == "freecad" and (not repo.freecad is None):
		openscad.FreeCADExporter().write_output(repo)


