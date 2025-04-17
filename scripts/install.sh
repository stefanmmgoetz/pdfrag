#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT

if [ ! -d env ]; then
	python -m venv env
	env/bin/pip install -r requirements.txt
else
	echo 'Program is already installed!'
fi

mkdir -p pdfs
