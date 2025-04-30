#!/bin/bash

ROOT=$(dirname $(dirname $0))
# source env/bin/python
cd $ROOT
source .env
IFS='|'
PDFS=($($BINDIR/zenity --file-selection --multiple --title="Upload PDFs" 2> /dev/null))

echo
newpdfs=0
for PDF in ${PDFS[@]}; do
	pdfname=$(basename $PDF)
	if [ -f pdfs/processed/$pdfname ]; then
		echo "[WARN]: $pdfname is already in the library"
	else
		cp $PDF pdfs/
		echo "[INFO]: added $pdfname"
		((newpdfs++))
	fi
done
echo

echo
if [ $newpdfs -gt 0 ]; then
	echo "[INFO]: $newpdfs new PDFs uploaded."
	echo '[INFO]: Updating database...'
	./src/update_db.sh
else
	echo '[WARN]: No new PDFs uploaded.'
fi
