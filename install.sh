#!/bin/bash

ROOT=$(dirname $0)
cd $ROOT

OS=$(uname)



if [[ ${OS} == 'Darwin' ]]; then
	if [ ! -d /opt/homebrew/bin ] && [ ! -d /usr/local/Homebrew/bin ]; then
		echo 'Homebrew not detected, installing homebrew...'
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	fi
	if [ -d /opt/homebrew/bin ]; then
		BREWDIR=/opt/homebrew/bin
		BINDIR=$BREWDIR
		echo 'export BINDIR='$BINDIR > .env
	elif [ -d /usr/local/Homebrew/bin ]; then
		BREWDIR=/usr/local/Homebrew/bin
	 	BINDIR=/usr/local/bin
		echo 'export BINDIR='$BINDIR > .env
	else
		echo 'Cannot find where the homebrew binary folder is...'
		exit 1
	fi
	if [ ! -f $BREWDIR/python3.9 ]; then
		echo 'Python 3.9 not detected, installing Python 3.9...'
		$BREWDIR/brew install python@3.9
	fi
	if [ ! -f $BREWDIR/zenity ]; then
		echo 'Zenity (for GUI) not detected, installing Zenity...'
		$BREWDIR/brew install zenity
	fi
	PYTHON=$BINDIR/python3.9
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
