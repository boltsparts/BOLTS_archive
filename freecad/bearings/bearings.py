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
import FreeCAD
import math

def makeRing(r1,r2):
	"""create a ring that can be used as a drop in replacement for torus to work around a performance problem"""
	res = Part.makeCylinder(r1+r2,2*r2).cut(Part.makeCylinder(r1-r2,3*r2))
	res.translate((0,0,-r2))
	return res


def singlerowradialbearing(params,document):
	rout=0.5*params['d2']
	rin=0.5*params['d1']
	bth=0.5*params['B']
	r_fillet=0.5*params['r_fillet']
	name=params['name']
	seal = params['type']

	#shapes
	shapes=[]
	RR=0.015*rout
	rb=(rout-rin)*0.25
	cb=((rout-rin)/2.00+rin)
	#outer ring
	our=Part.makeCylinder(rout,bth).cut(Part.makeCylinder(cb+rb*0.7,bth))
	our=our.makeFillet(r_fillet,our.Edges)
	#inner ring
	inr=Part.makeCylinder(cb-rb*0.7,bth).cut(Part.makeCylinder(rin,bth))
	inr=inr.makeFillet(r_fillet,inr.Edges)

	if seal == "open" or seal.endswith("single"):
		#track
		t=Part.makeCylinder(cb+rb,2*0.7*rb).cut(Part.makeCylinder(cb-rb,2*0.7*rb))
		t.translate((0,0,0.5*0.7*rb))
		our=our.cut(t)
		inr=inr.cut(t)
		shapes.append(our)
		shapes.append(inr)

		#Balls
		nb=int(math.floor(math.pi*cb*0.8/rb))
		for i in range (nb):
			b=Part.makeSphere(rb)
			Alpha=(i*2*math.pi)/nb
			bv=(cb*math.cos(Alpha),cb*math.sin(Alpha),bth/2)
			b.translate(bv)
			shapes.append(b)

		if seal.endswith("single"):
			#seal one side
			sl=Part.makeCylinder(cb+rb*0.9,0.5*bth-RR).cut(Part.makeCylinder(cb-rb*0.9,0.5*bth-RR))
			sl.translate((0,0,0.5*bth+RR))
			shapes.append(sl)

	elif seal.endswith("double"):
		shapes.append(our)
		shapes.append(inr)
		#seal
		sl=Part.makeCylinder(cb+rb*0.9,bth-2*RR).cut(Part.makeCylinder(cb-rb*0.9,bth-2*RR))
		sl.translate((0,0,RR))
		shapes.append(sl)

	part = document.addObject("Part::Feature","BOLTS_part")
	comp=Part.Compound(shapes)
	part.Shape=comp.removeSplitter()
	part.Label = name


def doublerowradialbearing(params,document): 
	rin=0.5*params['d1']
	rout=0.5*params['d2']
	bth=params['B']
	name = params['name']
	rb=0.3*(rout-rin)
	cb=(rout+rin)/2.0
	RR=0.015*rout

	shapes = []

	#outer ring
	our1=Part.makeCylinder(rout,bth)
	our2=Part.makeCylinder(cb+rb*0.7,bth)
	our3=Part.makeCylinder(rout,0.1*bth)
	our4=Part.makeCylinder(rout-0.12*(rout-rin),0.1*bth)
	our=our1.cut(our2)
	oursv=(0,0,0.45*bth)
	ours=our3.cut(our4)
	ours.translate(oursv)
	our=our.cut(ours)
	oure=our.Edges
	our=our.makeFillet(RR,oure)
	#inner ring
	inr1=Part.makeCylinder(cb-rb*0.7,bth)
	inr2=Part.makeCylinder(rin,bth)
	inr=inr1.cut(inr2)
	inre=inr.Edges
	inr=inr.makeFillet(RR,inre)
	#track
	t1=makeRing(cb,rb)
	t2=makeRing(cb,rb)
	vt1=(0,0,rb+bth/2)
	vt2=(0,0,(bth/2)-rb)
	t1.translate(vt1)
	t2.translate(vt2)
	our=our.cut(t1).cut(t2)
	inr=inr.cut(t1).cut(t2)
	#shapes
	shapes.append(our)
	shapes.append(inr)
	#Balls
	nb=(math.pi*cb)*0.8/(rb)
	nb=math.floor(nb)
	nb=int(nb)
	for i in range (nb):
		b=Part.makeSphere(rb)
		Alpha=(i*2*math.pi)/nb
		bv=(cb*math.cos(Alpha),cb*math.sin(Alpha),rb+bth/2)
		b.translate(bv)
		shapes.append(b) 
	
	offset=math.asin(rb/cb)
	for i in range(nb):
		b=Part.makeSphere(rb)
		Alpha=(i*2*math.pi)/nb
		bv=(cb*math.cos(Alpha+offset),cb*math.sin(Alpha+offset),(bth/2)-rb)
		b.translate(bv)
		shapes.append(b)

	part = document.addObject("Part::Feature","BOLTS_part")
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()
	part.Label = name


def axialthrustbearing(params, document):
	rin_w = 0.5*params['d_w']
	rin_g = 0.5*params['d_g']
	rout_w = 0.5*params['D_w']
	rout_g = 0.5*params['D_g']
	r_fillet =  params['r_fillet']
	bth = params['T']
	name = params['name']
	fth=0.3*bth  #Thrust plate widh

	shapes=[]

	#Lower ring
	lr1=Part.makeCylinder(rout_g,fth)
	lr2=Part.makeCylinder(rin_g,fth)
	lr=lr1.cut(lr2)
	lre=lr.Edges
	lr=lr.makeFillet(r_fillet,lre)
	#Upper ring
	ur1=Part.makeCylinder(rout_w,fth)
	ur2=Part.makeCylinder(rin_w,fth)
	ur=ur1.cut(ur2)
	ure=ur.Edges
	ur=ur.makeFillet(r_fillet,ure)
	#Positioning Vector
	Vur=(0,0,bth-fth)
	ur.translate(Vur)
	#Balltracks
	tbigradius=((rout_w-rin_g)/2.00)+rin_g
	tsmradius=(bth/2.00)-(0.75*fth)
	Vtorus=(0,0,bth/2.00)
	torus=makeRing(tbigradius,tsmradius)
	#Positioning vector
	torus.translate(Vtorus)
	#Booleans
	lr=lr.cut(torus)
	ur=ur.cut(torus)
	shapes.append(ur)
	shapes.append(lr)
	#Balls
	RBall=tsmradius
	CBall=tbigradius
	#Ball number (constant multiplied by radius and rounded)
	NBall=(2*math.pi*CBall)/(2*RBall)
	NBall=math.floor(NBall)
	NBall=NBall*0.9
	NBall=int(NBall)
	#Ball creator
	for i in range (NBall): 
		Ball=Part.makeSphere(RBall)
		Alpha=(i*2*math.pi)/NBall 
		BV=(CBall*math.cos(Alpha),CBall*math.sin(Alpha),bth/2.00)
		Ball.translate(BV)
		shapes.append(Ball)

	part = document.addObject("Part::Feature","BOLTS_part")
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()
	part.Label = name


def needlebearing(params, document):
	rout = 0.5*params["Ew"]
	rin = 0.5*params["Fw"]
	bth = params["Bc"]
	name = params['name']
	rnd=(rout-rin)/2.00
	cnd=((rout-rin)/2)+rin
	#Needle number
	nnd=2*math.pi*cnd/(1.8*2*rnd)
	nnd=int(math.floor(nnd))

	shapes=[]

	#needle cage
	ncrout=cnd+0.175*(rout-rin)
	ncrin=cnd-0.175*(rout-rin)
	nc1=Part.makeCylinder(ncrout,bth)
	nc2=Part.makeCylinder(ncrin,bth)
	nc=nc1.cut(nc2)
	#needle space on the cage-
	rsnd=rnd*1.2
	thsnd=bth*0.8
	for i in range(nnd):
		snd=Part.makeCylinder(rsnd,thsnd)
		Alpha=(i*2*math.pi)/nnd
		nv=(cnd*math.cos(Alpha),cnd*math.sin(Alpha),0.1*bth)
		snd.translate(nv)
		nc=nc.cut(snd)
	#Needle creation
	for i in range(nnd):
		nd=Part.makeCylinder(rnd,thsnd)
		Alpha=(i*2*math.pi)/nnd
		nv=(cnd*math.cos(Alpha),cnd*math.sin(Alpha),0.1*bth)
		nd.translate(nv)
		shapes.append(nd)
	shapes.append(nc)

	part = document.addObject("Part::Feature","BOLTS_part")
	comp = Part.Compound(shapes)
	part.Shape = comp.removeSplitter()
	part.Label = name


def cylindricalrollerbearing(params,document):
	rin = 0.5*params['d1']
	rout = 0.5*params['d2']
	bth = params['B']
	name = params['name']
	rcy=0.2*(rout-rin)
	ccy=(((rout-rin)/2.0)+rin)
	RR=0.01*rout
	ncy=(2*math.pi*ccy)*0.8/(2*rcy)
	ncy=math.floor(ncy)
	ncy=int(ncy)

	shapes = []

	#outer ring
	our1=Part.makeCylinder(rout,bth)
	our2=Part.makeCylinder(ccy+0.6*rcy,bth)
	our3=Part.makeCylinder(ccy+rcy,bth*0.6)
	ourv=(0,0,bth*0.2)
	our3.translate(ourv)
	our=our1.cut(our2)
	oure=our.Edges
	our.makeFillet(RR,oure)
	our=our.cut(our3)
	#inner ring
	inr1=Part.makeCylinder(ccy-rcy,bth)
	inr2=Part.makeCylinder(rin,bth)
	inr=inr1.cut(inr2)
	inre=inr.Edges
	inr.makeFillet(RR,inre)
	#shapes
	shapes.append(our)
	shapes.append(inr)
	#Cylinders
	ncy=(2*math.pi*ccy)*0.8/(2*rcy)
	ncy=math.floor(ncy)
	ncy=int(ncy)
	for i in range (ncy):
		c=Part.makeCylinder(rcy,0.6*bth)
		Alpha=(i*2*math.pi)/ncy
		cv=(ccy*math.cos(Alpha),ccy*math.sin(Alpha),bth*0.2)
		c.translate(cv)
		shapes.append(c)

	part = document.addObject("Part::Feature","BOLTS_part")
	comp=Part.Compound(shapes)
	part.Shape=comp.removeSplitter()
	part.Label = name
