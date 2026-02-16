#!/usr/bin/env bash

set -o errexit  # exit on error

pip install -r requirements.txt

cd locallibrary

python manage.py collectstatic --no-input
python manage.py migrate
python create_su.py