---
  title: New and better website for BOLTS
  date: 2014-09-10 13:30:00
  author: Johannes <jreinhardt@ist-dein-freund.de>
---

You are currently visiting the shiny new website of BOLTS that I have worked on
in the last few weeks. The old homepage was becoming more and more
unmaintainable, as it developed into a tangled mess of generated and manually
written content that was piped through Jekyll to be hosted as static html on
GitHub pages. The new page improves on that in several respects, and this is
what this post is about.

<!-- more -->

New url
-------

BOLTS now has a proper and more memorable domain at
[bolts-library.org](http://bolts-library.org), instead of a relatively
complicated github.io url. I had to take a domain with a additional suffix, as
bolts alone was already taken in every useful top level domain. Thats the
disadvantage if you choose an acronyme for a project that is also a real word.

Responsive Design
-----------------

The [original Jekyll Theme](https://github.com/Wolfr/cactus-jekyll-theme) that
I based the design of the BOLTS page on was responsive to a certain extent, but
I never spent the time to truly understand all the details, which resulted in a
very bad visual appearance on small devices. When it comes to web design, I am
most comfortable with [Bootstrap](http://getbootstrap.com), so I decided to
rebuild the homepage in Bootstrap. It looks a bit different now, but works much
better on tablets and phones.

Translations
------------

One of the main reason for the rebuild of the website was that I wanted to be
able to provide a localized user experience for people not so comfortable with
the english language. To manage translations I chose gettext (because it is a
very common format for this kind of tasks and is well supported by many tools)
and weblate (because it supports gettext and ties in very well with my work
flow).

All the translateable strings in BOLTS are collected in three different domains:

- `messages` contains all the strings of the webpage, mainly link labels
  for navigation, but also longer bits of text from the front page or other
  pages.
- `docs` contains all the documentation. I split up the big chunks of text
  in paragraphs to make it easier to translate and deal with changes in the
  content.
- `parts` contains all strings harvested from the parts data, mostly labels
  and descriptions intended for human consumption. This data will also be used
  to provide a localised experience for e.g. BOLTS for FreeCAD.

Translating all these strings (at the time of writing there are almost 1000
source strings with nearly 15000 words marked for translation) is something
that does not require as much technical knowledge as some of the other ways to
contribute to BOLTS. But it helps a lot, by making it easier for people from
all over the world to use BOLTS.

So I ask you to go over to our
[Weblate instance](https://weblate.stbuehler.de/projects/BOLTS/) and start
translating. You can choose which of the three domains (called subprojects in
weblate) you want to work on and which language you want to translate into.
Finally you can select a subset of strings to display, to translate hitherto
untranslated stuff choose `untranslated strings`, if you want to check existing
translations, choose `All strings` or another filter.

You can then suggest translations without being logged in or registered.
Suggestions need to be approved by a logged in translator, and can not be
attributed to you. To save translations and have them properly attributed in
the commit message, you can register an account for free, or if you have a
google or github account you can log in from these.

At the moment translations are set up for the four most popular languages of the
visitors of the old website, namely English, German, French and Spanish. If you
want to work on another language, just get in touch, e.g. by leaving a comment.

You can change the language with the language selector on the left of the
menubar. Untranslated content will still be displayed in english.

Full Text Search
----------------

Another functionality that I wanted to have and that was just not possible with
the old setup is a search feature. The search is accessible from the top menu
bar. It is language sensitive, i.e. will only search the localised version of
the website for your current language, so at the moment a lot of untranslated
content will still be found in english.

The results are clustered in two categories, parts and documentation, so that
you can easily select the result that you are interested in.

Versioned Documentation
-----------------------

Now the documentaion for multiple versions of BOLTS can be accessed separately.
With the old setup, a common problem was, that the documentation was updated
for the current development version of BOLTS, and therefore differed
significantly from what people actually had installed, which was confusing. Now
the documentation for the stable relaease and the development version can be
accessed separately

At the moment however, the documentation for the development version is not
fully up to date.

Better Technology
-----------------

All these improvements are possible because the new website is written in
[Python](https://www.python.org/) and the [Flask Micro Framework](http://flask.pocoo.org/), 
making use of libraries like [Babel](http://babel.pocoo.org/),
[Whoosh](https://pythonhosted.org/Whoosh/index.html) and
[Webassets](http://webassets.readthedocs.org/en/latest).

The resulting web application is hosted on
[OpenShift](https://www.openshift.com/) a Platform as a Service (PaaS) built by
RedHat, which integrates very well with the git based workflow that emerged for
the development of BOLTS.

This stack will also allow for further experiments, improvements and
extensions. For example it will be very easy to expose a REST API to all the
data BOLTS nows about, to allow other application to easily obtain informations
about standard parts.

Better Workflow
---------------

For me the new site results in a much more comfortable workflow. The old site
lived in a separate and highly diverged `gh-pages` branch, and updating the
page with data from the master branch required a fragile construction of helper
scripts and resulted in a bloated repository and many extra commits.

The new website lives in the master branch and is therefore much easier to
manage. Also no generated content (apart from downloads) is committed, which
reduces the growth of the repository. I probably should at some point clean up
the history of the repo, to cut down the size.


Disadvantages
-------------

There are a few small disadvantages though. Due to the migration all the Google
credit that the old page had accumulated is lost, so at the moment it is a bit
more difficult to find the new website by googling.

And everytime I push an update to the homepage, there is roughly half a minute
downtime. It is possible to avoid this, but this requires a few changes to the
app, and I have not yet tackled that.
