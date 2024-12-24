#!/bin/bash

python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
python3.11 manage.py collectstatic --noinput
python3.11 manage.py migrate --noinput