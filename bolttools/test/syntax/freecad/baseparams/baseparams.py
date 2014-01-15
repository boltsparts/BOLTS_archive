# coding=utf8
#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#Copyright (C) 2013 Javier Martínez García <jaeco@gmx.com>
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

import Part
import math


### DEEP GROOVE SINGLE ROW BALL BEARING ###------------------------------

def singlerowradialbearing(params,document):
	rout=0.5*params['d2']
	rin=0.5*params['d1']
	bth=0.5*params['B']
	name=params['name']
	detailed = params['detailed']

	#shapes---
	shapes=[]
	RR=0.015*rout
	if detailed:
		rb=(rout-rin)*0.25
		cb=((rout-rin)/2.00+rin)
		#outer ring--------------
		our1=Part.makeCylinder(rout,bth)
		our2=Part.makeCylinder(cb+rb*0.7,bth)
		our=our1.cut(our2)
		oure=our.Edges
		our=our.makeFillet(RR,oure)
		#inner ring--------------
		inr1=Part.makeCylinder(cb-rb*0.7,bth)
		inr2=Part.makeCylinder(rin,bth)
		inr=inr1.cut(inr2)
		inre=inr.Edges
		inr=inr.makeFillet(RR,inre)
		#track-------------------
		t=Part.makeTorus(cb,rb)
		vt=(0,0,bth/2)
		t.translate(vt)
		our=our.cut(t)
		inr=inr.cut(t)
		#shapes---
		shapes.append(our)
		shapes.append(inr)
		#Balls-------------------
		nb=(math.pi*cb)*0.8/(rb)
		nb=math.floor(nb)
		nb=int(nb)

		for i in range (nb):
			b=Part.makeSphere(rb)
			Alpha=(i*2*math.pi)/nb
			bv=(cb*math.cos(Alpha),cb*math.sin(Alpha),bth/2)
			b.translate(bv)
			shapes.append(b)
	else:
		body = Part.makeCylinder(rout,bth)
		hole = Part.makeCylinder(rin,bth)
		body = body.cut(hole)
		body = body.makeFillet(RR,body.Edges)
		shapes.append(body)

	part=document.addObject("Part::Feature",name)
	comp=Part.Compound(shapes)
	part.Shape=comp.removeSplitter()
