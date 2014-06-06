#.+
# .context    : BOLTS - Open Library of Technical Specifications
# .title      : flanges
# .kind       : BOLTS base function
# .author     : Fabrizio Pollastri <f.pollastri@inrim.it>
# .site       : Torino - Italy
# .creation   : 12-May-2014
# .license    : MIT <http://opensource.org/licenses/MIT>
#
# Copyright (c) 2014 Fabrizio Pollastri <f.pollastri@inrim.it>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#.-

from FreeCAD import Base
import Part


def plate_flange(params,document):
    d1 = params['d1']
    k = params['k']
    D = params['D']
    b = params['b']
    d2 = params['d2']
    bn = params['bn']
    name = params['name']

    part = document.addObject("Part::Feature","BOLTS_part")
    part.Label = name

    flange(d1,k,D,b,d2,bn,False,part)


def blind_flange(params,document):
    d1 = params['d1']
    k = params['k']
    D = params['D']
    b = params['b']
    d2 = params['d2']
    bn = params['bn']
    name = params['name']

    part = document.addObject("Part::Feature","BOLTS_part")
    part.Label = name

    flange(d1,k,D,b,d2,bn,True,part)


def flange(d1,k,D,b,d2,bn,blind,part):

    ## flange disk
    p0 = Base.Vector(0.,0.,0.)
    caxis = Base.Vector(0.,0.,1)
    disk = Part.makeCylinder(0.5 * D,b,p0,caxis)

    # if not a blind flange, make the inner hole.
    if not blind:
        hole = Part.makeCylinder(0.5 * d1,b,p0,caxis)
        disk = disk.cut(hole).removeSplitter()

    ## bolts holes
    h0 = Base.Vector(0.5 * k,0.,0.)
    hole = Part.makeCylinder(0.5 * d2,b,h0,caxis)
    holes = hole.copy()
    for i in range(1,int(bn)):
        nhole = hole.copy()
        nhole.rotate(p0,caxis,i * 360. / bn)
        holes = holes.fuse(nhole)
    # drill holes
    flange = disk.cut(holes).removeSplitter()

    ## chamfer all edges
    part.Shape = flange.makeChamfer(0.05 * b,flange.Edges)
