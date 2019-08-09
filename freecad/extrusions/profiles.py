# **************************************************************************************
# *                                                                                    *
# *    BOLTS - Open Library of Technical Specifications                                *
# *                                                                                    *
# *    Copyright (C) 2014 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>           *
# *                                                                                    *
# *    This library is free software; you can redistribute it and/or                   *
# *    modify it under the terms of the GNU Lesser General Public                      *
# *    License as published by the Free Software Foundation; either                    *
# *    version 2.1 of the License, or any later version.                               *
# *                                                                                    *
# *    This library is distributed in the hope that it will be useful,                 *
# *    but WITHOUT ANY WARRANTY; without even the implied warranty of                  *
# *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU                *
# *    Lesser General Public License for more details.                                 *
# *                                                                                    *
# *    You should have received a copy of the GNU Lesser General Public                *
# *    License along with this library; if not, write to the Free Software             *
# *    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA    *
# *                                                                                    *
# **************************************************************************************


import math

import Part
from FreeCAD import Vector
from DraftGeomUtils import fillet as draft_fillet


# ************************************************************************************************
def vslot20x20(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = 8 * [vslot_outline]
    fillets = [5, 17, 29, 41]
    corner_offset = 0
    circle_offsets = [0]

    face = vslot(symmetry, vertices, fillets, corner_offset, circle_offsets)

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()

    # color
    if params["finish"] == "Black":
        part.ViewObject.DiffuseColor = (0.1, 0.1, 0.1)


# ************************************************************************************************
def vslot20x40(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (-w, 0, True, True, False, False),
        (-w, 0, False, True, True, False),
        (-w, 0, True, False, True, False),
        (-w, 0, False, False, True, True),
        (-w, 0, True, True, True, True),
        (-w, 0, False, True, False, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = 12 * [vslot_outline]

    fillets = [5, 29, 41, 65]
    corner_offset = -1 * w
    circle_offsets = [0, -w]

    face = vslot(symmetry, vertices, fillets, corner_offset, circle_offsets)

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()

    # color
    if params["finish"] == "Black":
        part.ViewObject.DiffuseColor = (0.1, 0.1, 0.1)


# ************************************************************************************************
def vslot20x60(params, document):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (-w, 0, True, True, False, False),
        (-w, 0, False, True, True, False),
        (-2 * w, 0, True, True, False, False),
        (-2 * w, 0, False, True, True, False),
        (-2 * w, 0, True, False, True, False),
        (-2 * w, 0, False, False, True, True),
        (-2 * w, 0, True, True, True, True),
        (-2 * w, 0, False, True, False, True),
        (-w, 0, True, True, True, True),
        (-w, 0, False, True, False, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = 16 * [vslot_outline]

    # add fillets in reverse order, as this inserts additional edges
    fillets = [5, 41, 53, 89]
    corner_offset = -2 * w
    circle_offsets = [0, -w, -2 * w]

    face = vslot(symmetry, vertices, fillets, corner_offset, circle_offsets)

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()

    # color
    if params["finish"] == "Black":
        part.ViewObject.DiffuseColor = (0.1, 0.1, 0.1)


# ************************************************************************************************
def vslot20x80(params, document):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (-w, 0, True, True, False, False),
        (-w, 0, False, True, True, False),
        (-2 * w, 0, True, True, False, False),
        (-2 * w, 0, False, True, True, False),
        (-3 * w, 0, True, True, False, False),
        (-3 * w, 0, False, True, True, False),
        (-3 * w, 0, True, False, True, False),
        (-3 * w, 0, False, False, True, True),
        (-3 * w, 0, True, True, True, True),
        (-3 * w, 0, False, True, False, True),
        (-2 * w, 0, True, True, True, True),
        (-2 * w, 0, False, True, False, True),
        (-w, 0, True, True, True, True),
        (-w, 0, False, True, False, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = 20 * [vslot_outline]

    # add fillets in reverse order, as this inserts additional edges
    fillets = [5, 53, 65, 113]
    corner_offset = -3 * w
    circle_offsets = [0, -w, -2 * w, -3 * w]

    face = vslot(symmetry, vertices, fillets, corner_offset, circle_offsets)

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()

    # color
    if params["finish"] == "Black":
        part.ViewObject.DiffuseColor = (0.1, 0.1, 0.1)


# ************************************************************************************************
def tslot20x20(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = 8 * [tslot_outline]
    fillets = [5, 17, 29, 41]
    corner_offset = 0
    circle_offsets = [0]

    face = tslot(symmetry, vertices, fillets, [], [], corner_offset, circle_offsets)

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()


# ************************************************************************************************
def tslot20x20_three_slot(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = [tslot_outline] + 2 * [tslot_closed] + 5 * [tslot_outline]
    fillets = [5, 7, 19, 31]

    closed_symmetry = [
        (0, 0, False, True, False, False),
    ]
    closed_vertices = [tslot_closed_space]

    corner_offset = 0
    circle_offsets = [0]

    face = tslot(
        symmetry,
        vertices,
        fillets,
        closed_symmetry,
        closed_vertices,
        corner_offset,
        circle_offsets,
    )

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()


# ************************************************************************************************
def tslot20x20_two_slot(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = [tslot_outline] + 4 * [tslot_closed] + 3 * [tslot_outline]
    fillets = [5, 7, 9, 21]

    closed_symmetry = [
        (0, 0, False, True, False, False),
        (0, 0, False, False, True, False),
    ]
    closed_vertices = 2 * [tslot_closed_space]

    corner_offset = 0
    circle_offsets = [0]

    face = tslot(
        symmetry,
        vertices,
        fillets,
        closed_symmetry,
        closed_vertices,
        corner_offset,
        circle_offsets,
    )

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()


# ************************************************************************************************
def tslot20x20_two_slot_opp(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = (
        [tslot_outline]
        + 2 * [tslot_closed]
        + 2 * [tslot_outline]
        + 2 * [tslot_closed]
        + [tslot_outline]
    )
    fillets = [5, 7, 19, 21]

    closed_symmetry = [
        (0, 0, False, True, False, False),
        (0, 0, False, True, False, True),
    ]
    closed_vertices = 2 * [tslot_closed_space]

    corner_offset = 0
    circle_offsets = [0]

    face = tslot(
        symmetry,
        vertices,
        fillets,
        closed_symmetry,
        closed_vertices,
        corner_offset,
        circle_offsets,
    )

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()


# ************************************************************************************************
def tslot20x20_one_slot(
    params,
    document
):
    name = params["name"]
    le = params["l"]

    # due to symmetry this can be nicely decomposed
    # x offset, y offset, reverse, switch, mir_x, mir_y
    symmetry = [
        (0, 0, False, False, False, False),
        (0, 0, True, True, False, False),
        (0, 0, False, True, True, False),
        (0, 0, True, False, True, False),
        (0, 0, False, False, True, True),
        (0, 0, True, True, True, True),
        (0, 0, False, True, False, True),
        (0, 0, True, False, False, True),
    ]

    vertices = [tslot_outline] + 6 * [tslot_closed] + [tslot_outline]
    fillets = [5, 7, 9, 11]

    closed_symmetry = [
        (0, 0, False, True, False, False),
        (0, 0, False, False, True, False),
        (0, 0, False, True, False, True),
    ]
    closed_vertices = 3 * [tslot_closed_space]

    corner_offset = 0
    circle_offsets = [0]

    face = tslot(
        symmetry,
        vertices,
        fillets,
        closed_symmetry,
        closed_vertices,
        corner_offset,
        circle_offsets
    )

    part = document.addObject("Part::Feature", "BOLTS_part")
    part.Label = name

    part.Shape = face.extrude(Vector(0, 0, le)).removeSplitter()


# ************************************************************************************************
# helper
def fillet(
    lines,
    indices,
    radius
):
    """
    fillets the corner between the segments and their successors in lines indicated by indices
    """

    lines = lines[:]

    # sort them in descending order, as filleting inserts additional edges
    indices.sort()
    indices.reverse()

    for i in indices:
        lines[slice(i, i + 2)] = draft_fillet(lines[slice(i, i + 2)], radius)

    return lines


def assemble(
    symmetry,
    vertices,
    offset_global=(0, 0)
):
    """
    Assemble a wire from a list of symmetry information and a list of list of vertices

    symmetry information is a tuple of
        offset x, offset y, bool reverse, bool switch_comp, bool mirror_x, bool mirror_y
    """

    offset = Vector(offset_global[0], offset_global[1], 0)

    lines = []

    vlast = None
    vcur = None

    for sym, verts in zip(symmetry, vertices):
        o_x, o_y, reverse, switch, mir_x, mir_y = sym
        mir_x = -1 if mir_x else 1
        mir_y = -1 if mir_y else 1
        if reverse:
            verts = verts[::-1]

        if vcur is None:
            vcur = Vector(verts[0])
            if switch:
                vcur[0], vcur[1] = vcur[1], vcur[0]

            vcur[0] = mir_x * vcur[0] + o_x + offset[0]
            vcur[1] = mir_y * vcur[1] + o_y + offset[1]

        for v in verts[1:]:
            vlast = vcur
            vcur = Vector(v)
            if switch:
                vcur[0], vcur[1] = vcur[1], vcur[0]

            vcur[0] = mir_x * vcur[0] + o_x + offset[0]
            vcur[1] = mir_y * vcur[1] + o_y + offset[1]

            lines.append(Part.makeLine(vlast, vcur))
    return lines


# ************************************************************************************************
# profile size
w = 20


# ************************************************************************************************
# Vslot profile:

# the size of the inner square
d = 5.68 + 3 / math.sqrt(2)

# one eight of the outline
vslot_outline = [
    (0.5 * d, 0, 0),
    (0.5 * d, 0.5 * 5.68, 0),
    (0.5 * w - 1.8 - 1.64, 0.5 * w - 1.8 - 1.64 - 1.5 / math.sqrt(2), 0),
    (0.5 * w - 1.8, 0.5 * w - 1.8 - 1.64 - 1.5 / math.sqrt(2), 0),
    (0.5 * w - 1.8, 0.5 * 5.68, 0),
    (0.5 * w, 0.5 * 5.68 + 1.8, 0),
    (0.5 * w, 0.5 * w, 0)
]

space_symmetry = [
    (0, 0, False, False, True, False),
    (-w, 0, True, False, False, False),
    (-w, 0, False, False, False, True),
    (0, 0, True, False, True, True)
]

# big spaces
vslot_space = [
    (0.5 * d, 0, 0),
    (0.5 * d, 0.5 * 5.68, 0),
    (0.5 * w - 2.7, 0.5 * w - 1.8 - 1.96, 0),
    (0.5 * w - 2.7, 0.5 * w - 1.8, 0),
    (0.5 * w, 0.5 * w - 1.8, 0),
]

# corner holes
vslot_cornerhole = [
    (0.5 * w - 1.8, 0.5 * w - 1.8 - 1.64 - 1.5 / math.sqrt(2) + 1.07, 0),
    (0.5 * w - 1.8, 0.5 * w - 1.8, 0),
    (0.5 * w - 1.8 - 1.64 - 1.5 / math.sqrt(2) + 1.07, 0.5 * w - 1.8, 0),
    (0.5 * w - 1.8, 0.5 * w - 1.8 - 1.64 - 1.5 / math.sqrt(2) + 1.07, 0)
]


def vslot(
    symmetry,
    vertices,
    fillets,
    corner_offset,
    circle_offsets
):
    outline = assemble(symmetry, vertices)
    outline = fillet(outline, fillets, 1.5)
    outline = Part.Wire(outline)

    holes = []

    # corners
    # x offset, y offset, reverse, switch, mir_x, mir_y
    corner_symmetry = [
        (0, 0, False, False, False, False),
        (corner_offset, 0, False, False, True, False),
        (corner_offset, 0, False, False, True, True),
        (0, 0, False, False, False, True),
    ]

    for sym in corner_symmetry:
        holes.append(Part.Wire(assemble([sym], [vslot_cornerhole])))
        if sym[4] == sym[5]:
            holes[-1].reverse()

    # circular holes
    for offset in circle_offsets:
        holes.append(Part.Wire(Part.makeCircle(2.1, Vector(offset, 0, 0))))
        holes[-1].reverse()

    # big spaces
    print("Space")
    for offset in circle_offsets[:-1]:
        print(space_symmetry, vslot_space)
        holes.append(Part.Wire(assemble(space_symmetry, 4 * [vslot_space], (offset, 0))))
        holes[-1].reverse()
    print("Space")

    # put everything together
    return Part.Face([outline] + holes)


# ************************************************************************************************
# T slot profile:

# outline
tslot_outline = [
    (5.0, 0, 0),
    (5.0, 3.5, 0),
    (7.5, 6.0, 0),
    (9.0, 6.0, 0),
    (9.0, 3.0, 0),
    (10.0, 3.0, 0),
    (10.0, 10.0, 0),
]

# closed slots ouline
tslot_closed = [
    (10.0, 0.0, 0),
    (10.0, 10.0, 0),
]

# closed slots spaces
tslot_closed_space = [
    (5.0, 0, 0),
    (5.0, 3.5, 0),
    (7.5, 6.0, 0),
    (9.0, 6.0, 0),
    (9.0, -6.0, 0),
    (7.5, -6.0, 0),
    (5.0, -3.5, 0),
    (5.0, 0, 0),
]

# big spaces
tslot_space = [
    (0.5 * d, 0, 0),
    (0.5 * d, 0.5 * 5.68, 0),
    (0.5 * w - 2.7, 0.5 * w - 1.8 - 1.96, 0),
    (0.5 * w - 2.7, 0.5 * w - 1.8, 0),
    (0.5 * w, 0.5 * w - 1.8, 0),
]


def tslot(
    symmetry,
    vertices,
    fillets,
    closed_symmetry,
    closed_vertices,
    corner_offset,
    circle_offsets
):
    outline = assemble(symmetry, vertices)
    outline = fillet(outline, fillets, 1.5)
    outline = Part.Wire(outline)

    holes = []

    # closed holes
    for sym, vert in zip(closed_symmetry, closed_vertices):
        holes.append(Part.Wire(assemble([sym], [vert])))
        if not sym[5]:
            holes[-1].reverse()

    # circular holes
    for offset in circle_offsets:
        holes.append(Part.Wire(Part.makeCircle(2.25, Vector(offset, 0, 0))))
        holes[-1].reverse()

    # put everything together
    return Part.Face([outline] + holes)
