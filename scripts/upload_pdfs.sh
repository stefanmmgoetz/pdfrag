#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
PDFOLDER=$(/opt/homebrew/bin/zenity --file-selection --directory --title="Select PDF folder")
cp $PDFOLDER/*.pdf pdfs/
