#!/bin/sh
git checkout master -- output
mv output/html .
mv output/downloads/* .
