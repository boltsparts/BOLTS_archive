---
  title: Improvements for BOLTS for OpenSCAD
  author: Johannes <jreinhardt@ist-dein-freund.de>
  date: 2013-12-27 23:15:00
---

I am looking for ways to make it easier to use parts from
[BOLTS]({{ url(main.index) }})) in OpenSCAD. At the moment it is a bit awkward
because one has to know precisely how the BOLTS part is positioned and oriented
and then has to translate and rotate it around. This often requires the
knowledge of some dimensions of the part, so one has to query BOLTS about it,
and suddenly it is a lot of code that is difficult to read and annoying to
write.

<!-- more -->

OpenSCAD code in general quickly becomes big and difficult, because it usually
describes several solids with dimensions and positions that depend on each
other, so everything is quite entangled on a global scale. The module concept
allows for a certain degree of reuse, but I still often find myself in the
situation that I get stuck with understanding a piece of massively nested
OpenSCAD code that I wrote only a while ago. Things like 
translate\(\[h-2\*l,40-k,a+b+f-c\]\) rotate\(\[0,90,0\]\) translate\(...\).

### Scope

I believe that scope is a fundamental ingredient to clarity and brevity
in programming. Allowing the programmer to think only about the current
problem he is attacking, while moving everything else out of sight,
results in clean and readable code.

I had bookmarked obijuans
[attach library](https://github.com/Obijuan/obiscad)(or on
[Thingiverse](http://www.thingiverse.com/thing:30136)) already quite a while
ago, because I had hoped, that the connector concept could allow for cleaner,
less entangled code. When playing around with it, I realized that a connector
is basically a local coordinate system with a origin, one axis to fix the
direction and another axis to fix the rotation around the first axis.

I like the idea of local coordinate systems, because it is a local
scope that can be convenient to think in. It also seems a promising
approach to avoid or at least reduce the cumbersome and
difficult nested transformations or complicated arguments that I often
end up with.

I hacked together [a bit of code](https://github.com/jreinhardt/local-scad)
to do that, heavily inspired by the attach library, but working around some
issues. At the moment it allows to do three things:

* Create and display coordinate systems (lists of lists with origin and
  x,y,z axes, but the user should not need to know this)
* move and rotate an object (or a whole tree) from the global coordinate
  system into a local one.
* align a coordinate system and a object (or a tree) with
  another coordinate system.

The first and the last operation are slightly improved variations of
the functionality of the attach library.

### Positioning in BOLTS for OpenSCAD

To make use of this method of positioning in BOLTS, each part provides
a few connectors located at strategic positions of the part. Then the align
operation can be used to position and orient the part. This way things like
"put that bolt the so that its tip is here" or "the head of that bolt should
be at this point" can be expressed in a compact and readable way.

[<img alt="Connector positions" src="{{ static(openscad-connectors.png) }}" />]({{ static(openscad-connectors.png) }})

### Example: Bolted connection

    include <BOLTS.scad>
    
    $fn=50;
    
    % cube([10,40,50]);
    
    //connectors
    cube_cs = new_cs(origin = [10,20,20], axes = [[-1,0,0],[0,-1,0]]);
    washer_cs = ISO7089_conn("top","M4");
    bolt_cs = ISO4017_conn("root","M4",20);
    nut_cs = ISO4035_conn("bottom","M4");
    
    //connectors can be displayed with
    //show_cs(cube_cs);
    
    //thickness of washer
    s = get_dim(ISO7089_dims("M4"),"s");
    
    //position washer and bolt at the location specified by cube_cs
    align(washer_cs,cube_cs) ISO7089("M4");
    align(bolt_cs,cube_cs,[-s,0,0]) ISO4017("M4",20);
    align(washer_cs,cube_cs,[10+s,0,0]) ISO7089("M4");
    align(nut_cs,cube_cs,[10+s,0,0]) ISO4035("M4");


which is readable, compact and flexible. To change the position or
orientation of the bolted connection, one just has to change cube_cs.
Changing the size of the bolts and washers change M4 is also easy.

[<img alt="Bolted connection example" src="{{ static(openscad-positioningexample.png) }}" />]({{ static(openscad-positioningexample.png) }})

### Try it

You can try this functionality with the most recent development snapshot from
the [BOLTS page]({{ url(main.downloads) }}). Either place the contents of the
archive in the same directory as the .scad files that use BOLTS, or follow the
instructions on 
[how to install BOLTS for OpenSCAD]({{ doc_version(0.4, openscad,installation) }}).

Not all parts have connectors yet, but nuts, washers, hex bolts and
batteries do. The names of the connectors are listed in the OpenSCAD section of the
[part page]({{ url(parts.index) }}).

There is no documentation for this feature (apart from this blog post), because
I might still change the way things work.
