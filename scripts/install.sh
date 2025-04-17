#!/bin/bash

echo $0

if [ ! -d env ]; then
	python -m venv env
	env/bin/pip install -r requirements.txt
else
	echo 'Program is already installed!'
fi

mkdir -p pdfs
