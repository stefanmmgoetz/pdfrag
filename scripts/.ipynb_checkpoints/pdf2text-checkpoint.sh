#!/bin/bash

ls pdfs/*.pdf > /tmp/pdflist
pdfs=($(cat /tmp/pdflist))

for pdf in ${pdfs[@]}
do
	textfile=$(echo $pdf | sed 's,.pdf,.txt,g' | sed 's,pdfs/,txt/,g')
	pdftotext $pdf $textfile
done

