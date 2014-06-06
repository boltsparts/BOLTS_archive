#!/bin/sh
git checkout master -- output downloads
rm -rf html
mv output/html/* .
git add html
git rm -rfq output
git add html blog.html contribute.html contributors.html downloads.html index.html public_domain.html tasks.html unclear_license.html atom.xml no_drawing.png thingtracker.json
git show master:bolttools/doc/blt_spec_dev.rst | rst2html --template _spec_template.txt > doc/general/specification_dev.html
#cp bolttools/doc/processing.* doc/general
#git add doc/general/processing.* doc/general/specification.html
