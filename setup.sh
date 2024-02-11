#!/bin/bash

python -m pip install --upgrade pip
python -m pip install -r requirement.txt
python -m playwright install --with-deps
