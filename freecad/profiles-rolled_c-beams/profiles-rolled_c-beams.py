#BOLTS - Open Library of Technical Specifications
#Copyright (C) 2014 Bernd Hahnebach <bernd@bimstatik.org>
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
from Part import makeCircle, makeLine
import Part, Arch

def cbeam_parallel_flange(params,document):
        key = params['type']
        h = params['h']
        b = params['b']
        tf = params['tf']
        tw = params['tw']
        r = params ['r']
        l = params['l']
        name = params['name']

        # lower flange, starting at the ene of web, going against clockwise
        Vlf1 = Vector(0,(-h/2),0)
        Vlf2 = Vector(b,-h/2,0)
        Vlf3 = Vector(b,-h/2+tf,0)
        Vlf4 = Vector((tw+r),(-h/2+tf),0)
        Llf1 = makeLine(Vlf1,Vlf2)
        Llf2 = makeLine(Vlf2,Vlf3)
        Llf3 = makeLine(Vlf3,Vlf4)

        # upper flange, starting at the rigth web fillet, going clockwise
        Vuf1 = Vector(tw+r,(h/2-tf),0)
        Vuf2 = Vector(b,(h/2-tf),0)
        Vuf3 = Vector(b,h/2,0)
        Vuf4 = Vector(0,h/2,0)
        Luf1 = makeLine(Vuf1,Vuf2)
        Luf2 = makeLine(Vuf2,Vuf3)
        Luf3 = makeLine(Vuf3,Vuf4)

        # web, starting rigth bottom, going against clockwise
        Vw1 = Vector(tw,(-h/2+tf+r),0)
        Vw2 = Vector(tw,(h/2-tf-r),0)
        Lw1 = makeLine(Vw1,Vw2)
        Lw2 = makeLine(Vuf4 ,Vlf1)

        # center of the fillets, starting right bottom, going up
        Vfc1 = Vector((tw+r),(-h/2+tf+r),0)
        Vfc2 = Vector((tw+r),(h/2-tf-r),0)
        normal = Vector(0,0,1)
        Cfc1 = makeCircle(r,Vfc1,normal,180,270)
        Cfc2 = makeCircle(r,Vfc2,normal, 90,180)

        # putting the segments together make a wire, a face and extrude it
        W = Part.Wire([Llf1,Llf2,Llf3,Cfc1,Lw1,Cfc2,Luf1,Luf2,Luf3,Lw2])
        F = Part.Face(W)

        if params['arch']:
                part = Arch.makeStructure(name=name)

                prof = document.addObject("Part::Feature","Profile")
                prof.Shape = F
                part.Base = prof

                part.Height = l
        else:
                part = document.addObject("Part::Feature","BOLTS_part")
                part.Label = name

                beam = F.extrude(Vector(0,0,l))
                part.Shape = beam
