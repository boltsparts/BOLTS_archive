---
  layout: post
  title: BOLTS in Thing Tracker Network
  date: 2014-06-04 13:00:00
---

I just played around a bit with automatically publishing all the parts in BOLTS
in the [Thing Tracker Network](http://thingtracker.net/). The Thing Tracker
Network is an awesome and very important idea, although it is still in the
early stages of development.

<!-- more -->

The Thing  Tracker Network specifies a way to publish your 3D designs in a way
that is independent from any particular website, and thus opens the possibility
for a world without 
[walled gardens](https://en.wikipedia.org/wiki/Walled_garden_%28technology%29).

I will not go into details why walled gardens are bad for an ecosystem. But I
believe that there is still a chance to steer towards a world without walled
gardens for 3D designs for 3D printers. There are some big places around that
have a huge market share, but I think that the community that uses these
platforms is still flexible and open enough to make an unwalled solution a success.
This time slot closes though, the walls are getting higher, the users more lazy
and unwilling to change anything.

But the fundamental discussions aside, what I did is that I added an automatic
export of a TTN tracker for all the parts in BOLTS. It is available
[here (not for humans to read)]({{site.baseurl}}/thingtracker.json). That
turned out to be very easy to do, as all of the information necessary is
already available in computer readable and structured form. All it took were 50
lines of code.

As a user one can not do very much with it, apart from
[viewing the contents of the tracker](http://thingtracker.net/tools/viewer/?trackerURL={{site.baseurl}}/thingtracker.json#).
The only way in which this is or might be useful is to raise awareness and
activity for TTN and to help with the development of the TTN and of tools using
it.
