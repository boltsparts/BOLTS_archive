---
  title: Licensing issues
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

BOLTS is intended to be a project that incorporates contributions by many
different people and also allow to include existing code. This causes a number
of issues with respect to licensing.

<!-- more -->

There are two basic approaches to deal with these issues: Either be very
particular in what kind of license you want to have for all your content (which
is simple, but inflexible and you loose a certain pool of audience and
potential contributors), or be very careful about licenses and compatibility
(which is a lot more effort, but allows one to be more flexible and address a
larger audience).

I chose to lean more towards the second approach, and tried to automate the
license management as far as possible. From a technical point of view this was
surprisingly easy, it is very little additional code required. It took me much
more time to understand how this license stuff works and how to apply it to
BOLTS.

The result is a [document]({{ doc_version(0.3,general,licensing) }}) that I put into the
[documentation section]({{ url(docs.index) }}) (which is still rather empty,
but slowly filling up). This document describes my understanding of the license
related problems that BOLTS faces and describes how I chose to approach them
for BOLTS, and why.

In general I am progressing well with my work on BOLTS, the license stuff was
one of the last larger issues that I wanted to resolve before entering the next
stage and focus on writing documentation.
