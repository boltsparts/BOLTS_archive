---
  title: Website fixed
  date: 2015-01-29 11:00:00
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

An OpenShift update on 27 Jan 2015 broke something with the website. This should be fixed now.

<!-- more -->

I just noticed that the BOLTS website was broken. Looking at the logs it seemed
like a AppArmor adjustment lead to relative imports in the python code not
working anymore. I guess that this is a security fix, so I prefer that to break
instead of being vulnerable. Changing the relative imports to import relative
to the package seems to fix the problem.
