#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2014 Bernd Hahnebach <bernd@bimstatik.ch>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


from FreeCAD import Vector
from Part import makeBox
import Part
import math


def ibeam1(params,document):
        key = params['type']
        h = params['h']
        b = params['b']
        tf = params['tf']
        tw = params['tw']
        r = params ['r']
        l = params['l']
        name = params['name']



        part = document.addObject("Part::Feature","BOLTS_part")
        part.Label = name

        box1 = makeBox(b,tf,l)
        box1.translate(Vector(0,(h-tf),0))
        box2 = makeBox(b,tf,l)
        box3 = makeBox(tw,(h-2*tf),l)
        box3.translate(Vector((b/2),tf,0))
        beam =   box1.fuse(box2).fuse(box3)

        part.Shape = beam


        # fillet is missing
        # some profiles have radius = 0 because I don't know the radius yet

