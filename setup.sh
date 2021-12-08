#!/usr/bin/env bash
pip3 install --upgrade pip
pip3 install virtualenv
python3 -m venv assignment_env
source assignment_env/bin/activate

#pip freeze > requirements.txt
pip3 --no-cache-dir install -r requirements.txt
