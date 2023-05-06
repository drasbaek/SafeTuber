#!/usr/bin/env bash
# create virtual environment called lang_modelling_env
python3 -m venv safertube_env

# activate virtual environment
source ./safertube_env/bin/activate

# install requirements
python -m pip install -r requirements.txt

# install ffmpeg
#sudo apt update && sudo apt upgrade
sudo apt install ffmpeg