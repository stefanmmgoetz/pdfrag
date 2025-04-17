#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
echo $(pwd)

if [ ! -d env ]; then
	python -m venv env
	$ROOT/env/bin/pip install -r requirements.txt
else
	echo 'Program is already installed!'
fi

mkdir -p pdfs
