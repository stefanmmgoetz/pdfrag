#!/bin/bash

cd $(dirname $0)
cd ../src
TOKENIZERS_PARALLELISM=false ../env/bin/python ./main.py
