#!/usr/bin/env bash
# create virtual environment called lang_modelling_env
python3 -m venv safertube_env

# activate virtual environment
source ./safertube_env/bin/activate

# install requirements
python3 -m pip install -r requirements.txt

# run script for training and classifying
python3 src/yt-to-mp3.py

# deactivate virtual environment
deactivate safertube_env