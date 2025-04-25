#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT

OS=$(uname)

if [[ ${OS} == 'Darwin' ]]; then
	if [ ! -f /opt/homebrew/bin/brew ]; then
		echo 'Homebrew not detected, installing homebrew...'
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	fi
	if [ ! -f /opt/homebrew/bin/python3.9 ]; then
		echo 'Python 3.9 not detected, installing Python 3.9...'
		/opt/homebrew/bin/brew install python@3.9 zenity
	fi
	PYTHON=/opt/homebrew/bin/python3.9
else
	PYTHON=`which python`
fi

if [ ! -d env ]; then
	echo 'Installing Python dependencies...'
	$PYTHON -m venv env
	$ROOT/env/bin/pip install -r requirements.txt
else
	echo 'Program is already installed!'
fi

mkdir -p pdfs
