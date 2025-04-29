#!/bin/bash

ROOT=$(dirname $(dirname $0))
cd $ROOT
source env/bin/activate
cd src
TOKENIZERS_PARALLELISM=true ./main.py
