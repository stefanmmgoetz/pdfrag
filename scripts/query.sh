#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate

while true; do
	read -p 'Number of sentences: ' numsentences
	read -p 'Query: ' query
	python src/query_pdfs.py . $numsentences "$query" 2>/dev/null
done
	
