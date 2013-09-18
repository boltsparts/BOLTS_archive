#!/bin/sh
git checkout master -- output
rm -rf html downloads
mv output/html .
mv output/downloads/* .
rm -rf output
