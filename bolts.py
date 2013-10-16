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
from os import getcwd
import argparse

licenseids = {
	"lgpl2.1" : "LGPL 2.1",
	"lgpl2.1+" : "LGPL 2.1+",
	"lgpl3" : "LGPL 3.0",
	"lgpl3+" : "LGPL 3.0+",
	"gpl3" : "GPL 3.0",
	"gpl3+" : "GPL 3.0+"
}

def export(args):
	repo = blt_parser.BOLTSRepository(args.repo)
	license = licenseids[args.license]
	if args.target == "openscad":
		openscad.OpenSCADExporter().write_output(repo,license)
	elif args.target == "freecad":
		freecad.FreeCADExporter().write_output(repo,license)
	elif args.target == "html":
		html.HTMLExporter().write_output(repo)

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

args = parser.parse_args()
args.func(args)
