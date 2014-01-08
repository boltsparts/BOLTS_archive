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

from bolttools.blt import BOLTSRepository
from bolttools.freecad import FreeCADData
from bolttools.openscad import OpenSCADData
from bolttools.drawings import DrawingsData
from bolttools.solidworks import SolidWorksData

from backends.license import LICENSES_SHORT

from os import getcwd
from shutil import make_archive, copyfile
import os.path
from subprocess import call, Popen
import argparse
from datetime import datetime

#table is a list of lists, similar to the format html_table expects
def display_table(table,header,title,description):
	if len(table) == 0:
		return
	print title
	print '-'*len(title) + '\n'
	print description + '\n'

	#determine maximum field width
	width = []
	for field in header:
		width.append(len(field))
	for row in table:
		for i in range(len(row)):
			width[i] = max(len(str(row[i])),width[i])
	
	#add some more space
	for i in range(len(width)):
		width[i] += 2

	#print headers
	for i in range(len(header)):
		print "%-*s" % (width[i],header[i]),
	print ""
	for w in width:
		print "-"*w,
	print ""

	for row in table:
		for w,v in zip(width,row):
			print "%-*s" % (w,v),
		print ""
	print ""


def export(args):
	#load data
	repo = BOLTSRepository(args.repo)
	dbs = {}
	dbs["openscad"] = OpenSCADData(args.repo)
	dbs["freecad"] = FreeCADData(args.repo)
	dbs["drawings"] = DrawingsData(args.repo)
	dbs["solidworks"] = SolidWorksData(args.repo)

	license = LICENSES_SHORT[args.license]

	out_path = os.path.join(repo.path,"output",args.target)
	if args.target == "openscad":
		from backends.openscad import OpenSCADExporter
		OpenSCADExporter(repo,dbs).write_output(out_path,license,"development")
		copyfile(os.path.join(repo.path,"backends","licenses",args.license.strip("+")),
			os.path.join(out_path,"LICENSE"))
	elif args.target == "freecad":
		from backends.freecad import FreeCADExporter
		FreeCADExporter(repo,dbs).write_output(out_path,license,"development")
		copyfile(os.path.join(repo.path,"backends","licenses",args.license.strip("+")),
			os.path.join(out_path,"BOLTS","LICENSE"))
	elif args.target == "html":
		from backends.html import HTMLExporter
		HTMLExporter(repo,dbs).write_output(out_path)
	elif args.target == "solidworks":
		from backends.solidworks import SolidWorksExporter
		SolidWorksExporter(repo,dbs).write_output(out_path,"development")
	elif args.target == "iges":
		from backends.exchange import IGESExporter
		IGESExporter(repo,dbs).write_output(out_path,"development")

def test(args):
	exec_dir = os.path.join(args.repo,"output",args.target)
	if args.target == "freecad":
		freecad_process = Popen(["freecad","-M","."],cwd=exec_dir)
		freecad_process.wait()
	elif args.target == "openscad":
		freecad_process = Popen(["openscad"],cwd=exec_dir)
		freecad_process.wait()

def check(args):
	repo = BOLTSRepository(args.repo)
	dbs = {}
	dbs["openscad"] = OpenSCADData(args.repo)
	dbs["freecad"] = FreeCADData(args.repo)
	dbs["drawings"] = DrawingsData(args.repo)
	dbs["solidworks"] = SolidWorksData(args.repo)

	from backends.checker import CheckerExporter
	checker = CheckerExporter(repo,dbs)

	for check in checker.checks.values():
		print check.print_table()



def release(args):
	#check that there are no uncommited changes
	if call(["git","diff","--exit-code","--quiet"]) == 1:
		print "There are uncommited changes present in the git repository. Please take care of them before releasing"
		exit(1)

	if args.kind == "stable" and args.version is None:
		print "Please specify a version using -v when releasing a stable version"
		exit(2)
	if args.kind == "development" and not args.version is None:
		print "No explicit version can be given for development releases"
		exit(2)
	repo = BOLTSRepository(args.repo)

	version = datetime.now().strftime("%Y%m%d%H%M")
	stable = args.kind == "stable"
	if stable:
		version = args.version

	targets = [args.target]
	if targets[0] == "all":
		targets = ["freecad","openscad","iges"]

	from backends.openscad import OpenSCADExporter
	from backends.freecad import FreeCADExporter

	dbs = {}
	dbs["openscad"] = OpenSCADData(args.repo)
	dbs["freecad"] = FreeCADData(args.repo)

	backend_names = {"freecad" : "FreeCAD", "openscad" : "OpenSCAD", "iges" : "IGES"}

	#OpenSCAD, FreeCAD export
	for li_short in ["lgpl2.1+","gpl3"]:
		license = LICENSES_SHORT[li_short]
		OpenSCADExporter(repo,dbs).write_output(os.path.join(repo.path,"output","openscad"),license,version,stable)
		copyfile(os.path.join(repo.path,"backends","licenses",li_short.strip("+")),
			os.path.join(repo.path,"output","openscad","LICENSE"))
		FreeCADExporter(repo,dbs).write_output(os.path.join(repo.path,"output","freecad"),license,version,stable)
		copyfile(os.path.join(repo.path,"backends","licenses",li_short.strip("+")),
			os.path.join(repo.path,"output","freecad","BOLTS","LICENSE"))

		for backend in ["openscad", "freecad"]:
			if not backend in targets:
				continue
			backend_name = backend_names[backend]
			#construct filename from date
			template = "BOLTS_%s_%s_%s" % (backend_name,version,li_short)

			#create archives
			root_dir = os.path.join(repo.path,"output",backend)
			base_name = os.path.join(repo.path,"downloads",backend,template)
			make_archive(base_name,"gztar",root_dir)
			make_archive(base_name,"zip",root_dir)

	#iges export
	from backends.exchange import IGESExporter
	if "iges" in targets:
		try:
			import tarfile, lzma
		except ImportError:
			print "Could not find python-lzma, which is required for IGES export"
			return
		IGESExporter(repo,dbs).write_output(os.path.join(repo.path,"output","iges"),version,stable)

		#write xz file, see http://stackoverflow.com/a/13131500
		backend_name = backend_names["iges"]
		xz_name = "BOLTS_%s_%s.tar.xz" % (backend_name,version)
		xz_fid = lzma.LZMAFile(os.path.join(repo.path,"downloads","iges",xz_name),mode="w")
		with tarfile.open(mode="w", fileobj=xz_fid) as tar_xz_fid:
			tar_xz_fid.add(os.path.join(repo.path,"output","iges"),arcname="/")
		xz_fid.close()






parser = argparse.ArgumentParser()
parser.add_argument("--repo",
	type=str,
	help="path of the BOLTS repository to work on",
	default=getcwd())

subparsers = parser.add_subparsers()

parser_export = subparsers.add_parser("export")
parser_export.add_argument("target",
	type=str,
	choices=["openscad","freecad","html","solidworks","iges"],
	help="the distribution to create")
parser_export.add_argument("-l","--license",
	type=str,
	choices=["lgpl2.1","lgpl2.1+","lgpl3","lgpl3+","gpl3","gpl3+"],
	default="lgpl2.1",
	help="the license of the exported license")
parser_export.set_defaults(func=export)

parser_test = subparsers.add_parser("test")
parser_test.add_argument("target",
	type=str,
	choices=["openscad","freecad"],
	help="the backend to test")
parser_test.set_defaults(func=test)

parser_check = subparsers.add_parser("check")
parser_check.set_defaults(func=check)

parser_release = subparsers.add_parser("release")
parser_release.set_defaults(func=release)
parser_release.add_argument("kind",
	type=str,
	choices=["development","stable"],
	help="whether to create a development snapshot or a official relase",
	default="development")
parser_release.add_argument("target",
	type=str,
	choices=["all","openscad","freecad","iges"],
	default="all")
parser_release.add_argument("-v","--version",type=str)


args = parser.parse_args()
args.func(args)
