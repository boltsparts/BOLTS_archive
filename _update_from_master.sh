#!/bin/sh
git checkout master -- output
git rm -rfq html downloads
mv output/html .
mv output/downloads/* .
git rm -rfq output
git add html downloads
