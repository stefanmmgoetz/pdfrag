#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate
source .env

if [ ! -f secret.txt ]; then
	if [[ $(uname) == 'Darwin' ]]; then
		SECRET=$($BINDIR/zenity --file-selection --title="Select secret file")
		cp $SECRET secret.txt
	else
		echo 'API key file not detected... please drop secret.txt into the program directory to run queries.'
		read -p 'Press ENTER to continue.'
		exit 1
	fi
fi

read -p 'Number of sentences: ' numsentences
while true; do
	echo
	echo 'Querying PDF database...'
	read -p 'Query: ' query
	python src/query_pdfs.py . $numsentences "$query" 2>/dev/null || break
done
	
