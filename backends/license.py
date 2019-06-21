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

#Tools to manage license issues

#List of licenses BOLTS can handle
LICENSES = {
	"unclear" : "http://jreinhardt.github.io/BOLTS/unclear_license.html",
	"CC0 1.0" : "http://creativecommons.org/publicdomain/zero/1.0/",
	"Public Domain" : "http://jreinhardt.github.io/BOLTS/public_domain.html",
	# see https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT
	"MIT" : "http://opensource.org/licenses/MIT",
	"BSD 3-clause" : "http://opensource.org/licenses/BSD-3-Clause",
	"Apache 2.0" : "http://www.apache.org/licenses/LICENSE-2.0",
	"LGPL 2.1" : "http://www.gnu.org/licenses/lgpl-2.1",
	"LGPL 2.1+" : "http://www.gnu.org/licenses/lgpl-2.1",
	"LGPL 3.0" : "http://www.gnu.org/licenses/lgpl-3.0",
	"LGPL 3.0+" : "http://www.gnu.org/licenses/lgpl-3.0",
	"GPL 2.0+" : "http://www.gnu.org/licenses/gpl-2.0",
	"GPL 3.0" : "http://www.gnu.org/licenses/gpl-3.0",
	"GPL 3.0+" : "http://www.gnu.org/licenses/gpl-3.0",
}


LICENSES_SHORT = {
	"lgpl2.1" : "LGPL 2.1",
	"lgpl2.1+" : "LGPL 2.1+",
	"lgpl3" : "LGPL 3.0",
	"lgpl3+" : "LGPL 3.0+",
	"gpl3" : "GPL 3.0",
	"gpl3+" : "GPL 3.0+"
}


#Combinable pairs of licenses. (A,B) indicates that software with license A can
#be combined with software with license B and the combination has license B. See
#http://www.dwheeler.com/essays/floss-license-slide.html for details

#This is the place to make additions, all other representations of license
#compatibility are calculated from this

LICENSE_LINKS = [
	("Public Domain","MIT"),
	("CC0 1.0","MIT"),
	("MIT","BSD 3-clause"),
	("BSD 3-clause","Apache 2.0"),
	("BSD 3-clause","LGPL 2.1"),
	("BSD 3-clause","LGPL 2.1+"),
	("BSD 3-clause","LGPL 3.0"),
	("BSD 3-clause","LGPL 3.0+"),
	("Apache 2.0","LGPL 3.0+"),
	("Apache 2.0","LGPL 3.0"),
	("LGPL 2.1","GPL 2.0+"),
	("LGPL 2.1+","LGPL 2.1"),
	("LGPL 2.1+","LGPL 3.0"),
	("LGPL 2.1+","LGPL 3.0+"),
	("LGPL 2.1+","GPL 2.0+"),
	("LGPL 3.0","GPL 3.0"),
	("LGPL 3.0","GPL 3.0+"),
	("LGPL 3.0+","GPL 3.0"),
	("LGPL 3.0+","GPL 3.0+"),
	("GPL 2.0+","GPL 3.0"),
]

LICENSE_GRAPH = dict((k,[]) for k in LICENSES)
def _populate_license_graph():
	for a,b in LICENSE_LINKS:
		LICENSE_GRAPH[a].append(b)


_populate_license_graph()

def is_combinable_with(a,b):
	if a == b:
		return True
	if a not in LICENSES or b not in LICENSES:
		return False
	if b in LICENSE_GRAPH[a]:
		return True
	else:
		for child in LICENSE_GRAPH[a]:
			if is_combinable_with(child,b):
				return True
		return False

def is_license_supported(name):
	return name in LICENSES

def check_license(name,url):
	if name in LICENSES:
		return LICENSES[name] == url
	return False
