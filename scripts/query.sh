#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate

read -p 'Number of sentences: ' numsentences
read -p 'Query: ' query
python src/query_pdfs.py . $numsentences "$query"
