#!/bin/sh
git checkout master -- output
git rm -rfq html downloads
mv output/html .
mv output/downloads/* .
mv html/statistics.html _includes
git rm -rfq output
git add html downloads downloads.html
git add _includes/statistics.html
