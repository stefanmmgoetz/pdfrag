#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

OS=$(uname)

if [[ ${OS} == 'Darwin' ]]; then
	if [ ! -f /opt/homebrew/bin/brew ]; then
		echo 'Homebrew not detected, installing homebrew...'
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	fi
	if [ ! -f /opt/homebrew/bin/python3.9 ]; then
		echo 'Python 3.9 not detected, installing Python 3.9...'
		/opt/homebrew/bin/brew install python@3.9
	fi
	if [ ! -f /opt/homebrew/bin/zenity ]; then
		echo 'Zenity (for GUI) not detected, installing Zenity...'
		/opt/homebrew/bin/brew install zenity
	fi
	PYTHON=/opt/homebrew/bin/python3.9
else
	PYTHON=`which python`
fi

if [ ! -d env ]; then
	echo 'Installing Python dependencies...'
	$PYTHON -m venv env
	$ROOT/env/bin/pip install -r requirements.txt
	$ROOT/env/bin/pip install \
		--pre torch torchvision torchaudio \
		--extra-index-url https://download.pytorch.org/whl/nightly/cpu
else
	echo 'Program is already installed!'
fi

mkdir -p pdfs
