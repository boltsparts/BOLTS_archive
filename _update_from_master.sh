#!/bin/sh
git checkout master -- output
git rm -rfq html downloads
mv output/html .
mv output/downloads/* .
mv html/statistics.html _includes
git rm -rfq output
git add html downloads downloads.html
git add _includes/statistics.html
rst2html --template _spec_template.txt bolttools/doc/blt_spec_0_2.rst > doc/general/specification.html
cp bolttools/doc/processing.* doc/general
git add doc/general/processing.* doc/general/specification.html
