#!/bin/bash

refresh_directories () {
	mv mdd/*.md mdd/processed/
	mv pdfs/*.pdf pdfs/processed/
}

# NONINTERACTIVE=$1
ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate

mkdir -p {pdfs,mdd}/processed

echo 'Updating MDD directory...'
python src/pdf2mdd.py pdfs mdd

echo 'Updating vector database...'
PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 python src/gen_vector_db.py mdd bib && refresh_directories
echo 'Database is successfully updated! (unless you see big error message above lol)'
echo

# if [ -z $NONINTERACTIVE ]; then
# 	read -p '--- Press ENTER to continue ---'
# fi
