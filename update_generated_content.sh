#!/bin/sh

#update OpenSCAD distribution
python generate_scad.py

#update FreeCAD distribution
rm -rf output/freecad
mkdir output/freecad
cp freecad_bolts.py *.ui launch_freecad output/freecad
cp -r blt freecad output/freecad

#make tarballs
cd output/scad
tar -caf ../../downloads/openscad/BOLTS-OpenSCAD-`date +'%Y-%m-%d'`.tar.gz *
cd ..
cd freecad
tar -caf ../../downloads/freecad/BOLTS-FreeCAD-`date +'%Y-%m-%d'`.tar.gz *
cd ../..
tar -caf downloads/html/BOLTS-HTML-`date +'%Y-%m-%d'`.tar.gz html drawings

python generate_html.py

#commit to master
git commit -m "Automatic page update" html drawings downloads

#rebuild pages
git checkout gh-pages
git checkout master -- html
git checkout master -- drawings
git checkout master -- downloads
git add html drawings downloads
git commit -m "Automatic page update"
make local

git checkout master
