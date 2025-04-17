#!/bin/bash

if [ ! -d env ]; then
	python -m venv env
	env/bin/pip install -r requirements.txt
fi

PYTHON=env/bin/python
