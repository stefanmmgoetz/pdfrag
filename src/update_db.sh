#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate

# PDF2MDD_CMD="$ROOT/env/bin/python $ROOT/src/pdf2mdd.py $ROOT/pdfs $ROOT/mdd"
echo 'Updating MDD directory...'
python src/pdf2mdd.py pdfs mdd
# echo ${PDF2MDD_CMD}
# ${PDF2MDD_CMD}

# MDD2DB_CMD="$ROOT/env/bin/python $ROOT/src/gen_vector_db.py $ROOT/mdd $ROOT/bib"
echo 'Updating vector database...'
python src/gen_vector_db.py mdd bib
# echo ${MDD2DB_CMD}
echo 'Database is successfully updated! (unless you see big error message above lol)'
echo
read -p '--- Press ENTER to continue ---'

mkdir -p {pdfs,mdd}/processed
mv mdd/*.md mdd/processed/
mv pdfs/*.pdf pdfs/processed/
