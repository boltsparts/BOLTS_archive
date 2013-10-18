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
from bolttools.license import LICENSES_SHORT
from os import getcwd
from shutil import make_archive
import os.path
from subprocess import call, Popen
import argparse
from datetime import datetime


def export(args):
	repo = blt_parser.BOLTSRepository(args.repo)
	license = LICENSES_SHORT[args.license]
	if args.target == "openscad":
		openscad.OpenSCADExporter().write_output(repo,license)
	elif args.target == "freecad":
		freecad.FreeCADExporter().write_output(repo,license)
	elif args.target == "html":
		html.HTMLExporter().write_output(repo)

def test(args):
	if args.target == "freecad":
		exec_dir = os.path.join(args.repo,"output","freecad")
		freecad_process = Popen(["freecad","-M","."],cwd=exec_dir)
		freecad_process.wait()
	elif args.target == "openscad":
		exec_dir = os.path.join(args.repo,"output","openscad")
		freecad_process = Popen(["openscad"],cwd=exec_dir)
		freecad_process.wait()

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
	repo = blt_parser.BOLTSRepository(args.repo)

	#export
	html.HTMLExporter().write_output(repo)
	for li_short in ["lgpl2.1+","gpl3"]:
		license = LICENSES_SHORT[li_short]
		openscad.OpenSCADExporter().write_output(repo,license)
		freecad.FreeCADExporter().write_output(repo,license)

		for backend,backend_name in zip(["freecad","openscad"],["FreeCAD","OpenSCAD"]):
			#construct filename from date
			if args.kind == "development":
				date = datetime.now().strftime("%Y%m%d%H%M")
				template = "BOLTS_%s_%s_%s" % (backend_name,date,li_short)
			elif args.kind == "stable":
				template = "BOLTS_%s_%s_%s" % (backend_name,args.version,li_short)

			#create archives
			root_dir = os.path.join(repo.path,"output",backend)
			base_name = os.path.join(repo.downloads.out_root,"downloads",backend,template)
			make_archive(base_name,"gztar",root_dir)
			make_archive(base_name,"zip",root_dir)

	#write html overview
	downloads.DownloadsExporter().write_output(repo)


parser = argparse.ArgumentParser()
parser.add_argument("--repo",
	type=str,
	help="path of the BOLTS repository to work on",
	default=getcwd())

subparsers = parser.add_subparsers()
parser_export = subparsers.add_parser("export")
parser_export.add_argument("target",
	type=str,
	choices=["openscad","freecad","html"],
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

parser_release = subparsers.add_parser("release")
parser_release.set_defaults(func=release)
parser_release.add_argument("kind",
	type=str,
	choices=["development","stable"],
	help="whether to create a development snapshot or a official relase",
	default="development")
parser_release.add_argument("-v","--version",type=str)


args = parser.parse_args()
args.func(args)
