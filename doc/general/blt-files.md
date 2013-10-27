---
  layout: docs
  title: How to work with blt files
  docroot: "../"
---

blt files contain most of the basefile independent data. There is one blt file
for each each collection.

### Creating a new collection

To create a new collection a new file with extension blt needs to be created in
the `data` directory of the BOLTS repository. This file is a
[YAML](http://yaml.org/) file and contains a license header, a collection
header and a list of class descriptions.

The headers contains general information about the collection. This is an
example taken from the 
[hex collection]({{site.baseurl}}/html/collections/hex.html)
, and illustrates the form of the header. For detailed information please refer to the
[specification](http://127.0.0.1:4000/doc/general/specification.html#collection-header):

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
    ---
    collection:
        name: BOLTS hexagon fasteners
        description: various standard hex bolts and screws
        author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
        license: LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>
        blt-version: 0.2
    .
    .
    .

The license header (everything with a # at the beginning) specifies the license
of this particular file. The three dashes indicate the begin of the YAML
document. The collection header specifies the name, description, author,
license of the file and the blt-file version which this file follows.  YAML
uses indentation to mark up the structure of the document, so pay attention to
whitespace and do not use tabs. The amount of spaces for a indentation level is
arbitrary, but four spaces is recommended.

A email address must be given for the author, to have a way of contacting the
author e.g. for licensing problems.  The license in the license field and the
license header must agree and be one of the [licenses that BOLTS
allows](licensing.html). If more than one person contributed significantly,
then a list of authors can be given:

    author: [Johannes Reinhardt <jreinhardt@ist-dein-freund.de>, John Doe <doe@domain.tld>]

The next section describes how to add classes description to the empty class.

### Adding classes to a collection

After the header follows a list of class descriptions. One of the most
important informations contained there are the different parameters of the
part, their types, units and tables that connect them. Parameters can be
dimensions of the part (e.g. those indicated in the drawing), but also things
like components of the part name. They can either be set to a fixed value,
looked up in a table or left free to be set by the user.

Here is another example to illustrate the form of this part of the blt file:

    collection:
        name: BOLTS hexagon fasteners
        description: various standard hex bolts and screws
        author: Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
        license: LGPL 2.1+ <http://www.gnu.org/licenses/lgpl-2.1>
        blt-version: 0.2
    classes:
      - id: hexscrew1
        naming:
            template:  Hexagon head screw %s - %s %d
            substitute: [standard, key, l]
        drawing: hex/hex1.png
        description: hexagon head screw
        standard: DIN933
        status: withdrawn
        parameters:
            free: [key, l]
            types: {key: Table Index}
            defaults: {key: M3, l: 20}
            tables:
                index: key
                columns: [d1, k, s, e, h]
                data:
                    #key   [  d1    k      s     e        h     ]
                    M1.6:  [  1.6,  1.1,   3.2,  3.48,    None  ]
                    M2:    [  2,    1.4,   4,    4.32,    None  ]
                    M2.5:  [  2.5,  1.7,   5,    5.45,    None  ]
                    M3:    [  3,    2,     5.5,  6.01,    1.5   ]
                    M3.5:  [  3.5,  2.4,   6,    6.58,    None  ]
                    M4:    [  4,    2.8,   7,    7.66,    2.1   ]
                    M5:    [  5,    3.5,   8,    8.79,    2.4   ]
                    M6:    [  6,    4,     10,   11.05,   3     ]
                    M7:    [  7,    4.8,   11,   12.12,   None  ]
                    M8:    [  8,    5.3,   13,   14.38,   3.75  ]
                    M10:   [  10,   6.4,   17,   18.90,   4.5   ]
                    M12:   [  12,   7.5,   19,   21.10,   5.25  ]
                    M14:   [  14,   8.8,   22,   24.49,   6     ]
                    M16:   [  16,   10,    24,   26.75,   6     ]
                    M18:   [  18,   11.5,  27,   30.14,   7.5   ]
                    M20:   [  20,   12.5,  30,   33.53,   7.5   ]
                    M22:   [  22,   14,    32,   35.72,   7.5   ]
                    M24:   [  24,   15,    36,   39.98,   9     ]
                    M27:   [  27,   17,    41,   45.20,   9     ]
                    M30:   [  30,   18.7,  46,   50.85,   10.5  ]
                    M33:   [  33,   21,    50,   55.37,   10.5  ]
                    M36:   [  36,   22.5,  55,   60.79,   12    ]
                    M39:   [  39,   25,    60,   66.44,   None  ]
                    M42:   [  42,   26,    65,   71.30,   None  ]
                    M45:   [  45,   28,    70,   76.95,   None  ]
                    M48:   [  48,   30,    75,   82.60,   None  ]
                    M52:   [  52,   33,    80,   88.25,   None  ]
                    M64:   [  64,   40,    95,   104.86,  None  ]
        source: http://almetal.nl/en/techinfo/hex/hd933.htm
      - id: hexscrew2
        naming:
            template: Hexagon head screw %s - %s %d
            substitute: [standard, key, l]
        drawing: hex/hex1.png
    .
    .
    .

The class descriptions are the items of a YAML list, as indicated by the
hyphen. Again there are a number of fields, whose meaning can be looked up in the
[specification](http://127.0.0.1:4000/doc/general/specification.html#class-element).
Or you check out the other blt files to see what fields need to be given.
