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

def rectangle_hollow(params,document):
        h = params['h']
        b = params['b']
        t = params['t']
        l = params['l']
        name = params['name']

        ## Definition in EN standard
        ri=1.0*t
        ro=1.5*t

        # outer rectangle, going clockwise
        Vor1 = Vector((b/2),(h/2-ro),0)
        Vor2 = Vector((b/2),(-h/2+ro),0)
        Vor3 = Vector((b/2-ro),(-h/2),0)
        Vor4 = Vector((-b/2+ro),-h/2,0)
        Vor5 = Vector(-b/2,(-h/2+ro),0)
        Vor6 = Vector(-b/2,(h/2-ro),0)
        Vor7 = Vector((-b/2+ro),(h/2),0)
        Vor8 = Vector((b/2-ro),(h/2),0)
        Lor1 = makeLine(Vor1,Vor2)
        Lor2 = makeLine(Vor3,Vor4)
        Lor3 = makeLine(Vor5,Vor6)
        Lor4 = makeLine(Vor7,Vor8)

        # outer radius, going clockwise
        Voc1 = Vector((b/2-ro),(-h/2+ro),0)
        Voc2 = Vector((-b/2+ro),(-h/2+ro),0)
        Voc3 = Vector((-b/2+ro),(h/2-ro),0)
        Voc4= Vector((b/2-ro),(h/2-ro),0)
        normal = Vector(0,0,1)
        Coc1 = makeCircle(ro,Voc1,normal,270,  0)
        Coc2 = makeCircle(ro,Voc2,normal,180,270)
        Coc3 = makeCircle(ro,Voc3,normal, 90,180)
        Coc4 = makeCircle(ro,Voc4,normal,  0, 90)

        # inner rectangle, going clockwise
        Vir1 = Vector((b/2-t),(h/2-t-ri),0)
        Vir2 = Vector((b/2-t),(-h/2+t+ri),0)
        Vir3 = Vector((b/2-t-ri),(-h/2+t),0)
        Vir4 = Vector((-b/2+t+ri),(-h/2+t),0)
        Vir5 = Vector((-b/2+t),(-h/2+t+ri),0)
        Vir6 = Vector((-b/2+t),(h/2-t-ri),0)
        Vir7 = Vector((-b/2+t+ri),(h/2-t),0)
        Vir8 = Vector((b/2-t-ri),(h/2-t),0)
        Lir1 = makeLine(Vir1,Vir2)
        Lir2 = makeLine(Vir3,Vir4)
        Lir3 = makeLine(Vir5,Vir6)
        Lir4 = makeLine(Vir7,Vir8)

        # inner radius, going clockwise
        Vic1 = Vector((b/2-t-ri),(-h/2+t+ri),0)
        Vic2 = Vector((-b/2+t+ri),(-h/2+t+ri),0)
        Vic3 = Vector((-b/2+t+ri),(h/2-t-ri),0)
        Vic4= Vector((b/2-t-ri),(h/2-t-ri),0)
        normal = Vector(0,0,1)
        Cic1 = makeCircle(ri,Vic1,normal,270,  0)
        Cic2 = makeCircle(ri,Vic2,normal,180,270)
        Cic3 = makeCircle(ri,Vic3,normal, 90,180)
        Cic4 = makeCircle(ri,Vic4,normal,  0, 90)

        # putting the segments together, make wires, make faces, extrude them and cut them
        Wo = Part.Wire([Lor1,Coc1,Lor2,Coc2,Lor3,Coc3,Lor4,Coc4,])
        Wi = Part.Wire([Lir1,Cic1,Lir2,Cic2,Lir3,Cic3,Lir4,Cic4,])
        face = Part.Face([Wo,Wi])

        if params['arch']:
                part = Arch.makeStructure(name=name)

                prof = document.addObject("Part::Feature","Profile")
                prof.Shape = face
                part.Base = prof

                part.Height = l
        else:
                part = document.addObject("Part::Feature","BOLTS_part")
                part.Label = name

                beam = face.extrude(Vector(0,0,l))
                part.Shape = beam



def square_hollow(params,document):
        b = params['b']
        t = params['t']
        l = params['l']
        name = params['name']

        ## Definition in EN standard
        ri=1.0*t
        ro=1.5*t

        # outer rectangle, going clockwise
        Vor1 = Vector((b/2),(b/2-ro),0)
        Vor2 = Vector((b/2),(-b/2+ro),0)
        Vor3 = Vector((b/2-ro),(-b/2),0)
        Vor4 = Vector((-b/2+ro),-b/2,0)
        Vor5 = Vector(-b/2,(-b/2+ro),0)
        Vor6 = Vector(-b/2,(b/2-ro),0)
        Vor7 = Vector((-b/2+ro),(b/2),0)
        Vor8 = Vector((b/2-ro),(b/2),0)
        Lor1 = makeLine(Vor1,Vor2)
        Lor2 = makeLine(Vor3,Vor4)
        Lor3 = makeLine(Vor5,Vor6)
        Lor4 = makeLine(Vor7,Vor8)

        # outer radius, going clockwise
        Voc1 = Vector((b/2-ro),(-b/2+ro),0)
        Voc2 = Vector((-b/2+ro),(-b/2+ro),0)
        Voc3 = Vector((-b/2+ro),(b/2-ro),0)
        Voc4= Vector((b/2-ro),(b/2-ro),0)
        normal = Vector(0,0,1)
        Coc1 = makeCircle(ro,Voc1,normal,270,  0)
        Coc2 = makeCircle(ro,Voc2,normal,180,270)
        Coc3 = makeCircle(ro,Voc3,normal, 90,180)
        Coc4 = makeCircle(ro,Voc4,normal,  0, 90)

        # inner rectangle, going clockwise
        Vir1 = Vector((b/2-t),(b/2-t-ri),0)
        Vir2 = Vector((b/2-t),(-b/2+t+ri),0)
        Vir3 = Vector((b/2-t-ri),(-b/2+t),0)
        Vir4 = Vector((-b/2+t+ri),(-b/2+t),0)
        Vir5 = Vector((-b/2+t),(-b/2+t+ri),0)
        Vir6 = Vector((-b/2+t),(b/2-t-ri),0)
        Vir7 = Vector((-b/2+t+ri),(b/2-t),0)
        Vir8 = Vector((b/2-t-ri),(b/2-t),0)
        Lir1 = makeLine(Vir1,Vir2)
        Lir2 = makeLine(Vir3,Vir4)
        Lir3 = makeLine(Vir5,Vir6)
        Lir4 = makeLine(Vir7,Vir8)

        # inner radius, going clockwise
        Vic1 = Vector((b/2-t-ri),(-b/2+t+ri),0)
        Vic2 = Vector((-b/2+t+ri),(-b/2+t+ri),0)
        Vic3 = Vector((-b/2+t+ri),(b/2-t-ri),0)
        Vic4= Vector((b/2-t-ri),(b/2-t-ri),0)
        normal = Vector(0,0,1)
        Cic1 = makeCircle(ri,Vic1,normal,270,  0)
        Cic2 = makeCircle(ri,Vic2,normal,180,270)
        Cic3 = makeCircle(ri,Vic3,normal, 90,180)
        Cic4 = makeCircle(ri,Vic4,normal,  0, 90)

        # putting the segments together, make wires, make faces, extrude them and cut them
        Wo = Part.Wire([Lor1,Coc1,Lor2,Coc2,Lor3,Coc3,Lor4,Coc4,])
        Wi = Part.Wire([Lir1,Cic1,Lir2,Cic2,Lir3,Cic3,Lir4,Cic4,])
        face = Part.Face([Wo,Wi])

        if params['arch']:
                part = Arch.makeStructure(name=name)

                prof = document.addObject("Part::Feature","Profile")
                prof.Shape = face
                part.Base = prof

                part.Height = l
        else:
                part = document.addObject("Part::Feature","BOLTS_part")
                part.Label = name

                beam = face.extrude(Vector(0,0,l))
                part.Shape = beam


def circle_hollow(params,document):
        od = params['D']
        t = params['t']
        l = params['l']
        name = params['name']

        id = od - t

        outer = Part.Wire(Part.makeCircle(0.5*od))
        inner = Part.Wire(Part.makeCircle(0.5*id))
        face = Part.Face([outer,inner])

        if params['arch']:
                part = Arch.makeStructure(name=name)

                prof = document.addObject("Part::Feature","Profile")
                prof.Shape = face
                part.Base = prof

                part.Height = l
        else:
                part = document.addObject("Part::Feature","BOLTS_part")
                part.Label = name

                beam = face.extrude(Vector(0,0,l))
                part.Shape = beam
