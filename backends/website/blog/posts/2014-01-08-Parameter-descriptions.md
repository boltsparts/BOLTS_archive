---
  title: Parameter description
  date: 2014-01-08 16:15:00
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

blt files now contain a human readable description of the various  parameters
of a part.

<!-- more -->

I just merged some code that extends the blt file format to allow for short
descriptions of the parameters. The way this is specified is best shown with a
real world example (taken from
[here](https://github.com/jreinhardt/BOLTS/blob/master/data/nut.blt):


    - id: hexagonthinnut1
      naming:
        template: Hexagon thin nut %s - %s
        substitute: [standard, key]
      description: hexagon thin nuts
      standard: [ISO4035, DINENISO4035]
      replaces: DIN439B
      parameters:
          free: [key]
          types: {key: Table Index}
          defaults: {key: M3}
          description:
            key: Thread designation
            d1: hole diameter
            s: width across flats
            e_min: head diameter
            m_max: thickness
          tables:
              index: key
              columns: [d1, s, m_max, e_min]
              data:
                  #key    [  d1    s     m_max   e_min   ]
                  M1.6:   [  1.6,  3.2,  1,      3.48,   ]
                  M1.7:   [  1.7,  3.2,  1,      3.48,   ]
                  M2:     [  2,    4,    1.2,    4.32,   ]
                  M2.3:   [  2.3,  4.5,  1.2,    5.2,    ]
                  M2.5:   [  2.5,  5,    1.6,    5.45,   ]
    ...

The description field of the parameters element is a YAML associative array
that maps each parameter name to its description. If a part contains only few
parameters, the compact notation for associative arrays can be used (like in
the the types and defaults fields).

BOLTS has a check to encourage complete coverage of all parameters and
complains if unknown parameters are described.

This information is used in the [html documentation]({{ standard_url(ISO4035) }})
for each part, just below the drawing, to give it more context.

It is also shown as a tooltip in the FreeCAD widget, when hovering above the
widget for the free parameters:

[<img alt="Descriptive Tooltips" src="{{ static(freecad_tooltip.png) }}" />]({{ static(freecad_tooltip.png) }})

This feature (along with a few more improvements and fixes) is available in the
latest development snapshot from the [download section]({{ url(main.downloads) }}).
