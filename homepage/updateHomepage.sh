#!/bin/bash

# This script updates the homepage (branch: gh-pages)
# according the folder 'homepage' under the master branch

# Clean up previous builds
make clean

# Create html files
make html

# Copy relevant html content into a temporary folder
TMP_DIR=`mktemp -d`
cp -r _build/html "$TMP_DIR"/.
rm -rf _build

# Switch to gh-pages branch
cd ..
git checkout gh-pages

# Update content
rm -rf *
cp -r "$TMP_DIR"/html/* .

# Submit changes with current timestamp
TIMESTAMP=`date +'%Y-%m-%d %H:%M:%S'`
git add *
git commit -a -m "Homepage update ${TIMESTAMP}"
git push origin gh-pages

# Remove temporary folder
rm -rf "$TMP_DIR"

# Go back to the folder 'homepage' on the master branch
git checkout master
cd homepage/

# Create PDF file
make latexpdf

# Update PDF file
cp _build/latex/NipypeBeginnersGuide.pdf ../NipypeBeginnersGuide.pdf

# Clean up latexpdf build
make clean

# Submit newest PDF with current timestamp to homepage
git add ../NipypeBeginnersGuide.pdf
git commit -m "PDF update ${TIMESTAMP}"
git push origin master
