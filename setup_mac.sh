#!/usr/bin/env bash
# create virtual environment called safertube_env
python3 -m venv safertube_env

# activate virtual environment
source ./safertube_env/bin/activate

# install requirements
python3 -m pip install -r requirements.txt

# install ffmpeg
brew install ffmpeg

# bug where environment needs to be reactivated after installing ffmpeg
source ./safertube_env/bin/activate
