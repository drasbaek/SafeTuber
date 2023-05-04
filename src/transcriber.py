from pytube import Channel
from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline
import torch
from utils import *
import pandas as pd
import os
import random
import io
import sys

def define_paths():
    # define path
    path = Path(__file__)

    # define inpath
    inpath = path.parents[1] / "data" / "top-youtubers-curated.csv"

    # define outpath
    outpath = path.parents[1] / "data"

    # create dir for audio files if it doesn't exist
    if not os.path.exists(path.parents[1] / "audio_files"):
        os.makedirs(path.parents[1] / "audio_files")
    
    # define path to temporary audio storage
    audio_path = path.parents[1] / "audio_files"

    return inpath, outpath, audio_path

def get_channel_vids(channel_url):
    """
    Uses yt_dlp to get the video urls from a channel url.
    It is necessary to obtain these urls from the terminal output as extract_info does not return those
    """
    print("Getting video urls...")

    # Create a StringIO object to capture stdout
    captured_output = io.StringIO()

    # Redirect stdout to the StringIO object
    sys.stdout = captured_output

    # Run your code
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'playlistend': 10}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(
            channel_url,
            download=False
        )

    # Restore stdout to its original value
    sys.stdout = sys.__stdout__

    # Print the captured output
    output = captured_output.getvalue()

    # extract all urls from output
    urls = []

    for line in output.splitlines():
        if "https://www.youtube.com/watch?v=" in line:
            # extract only the url from the line
            url = line.split(" ")[-1]
            urls.append(url)

    return urls

def download_mp4(outpath, url, max_duration, min_duration):
    # get info
    ydl = YoutubeDL()
    info_dict = ydl.extract_info(url, download=False)

    # check duration
    duration = info_dict.get('duration')

    # if duration is too long, skip
    if duration > 1200:
        print("Video too long, skipping to next..." + url)
        return 0 # return 0 for fail
    
    if duration < 120:
        print("Video too short, skipping to next..." + url)
        return 0 # return 0 for fail

    # else download
    else:
        ydl_opts = {
        'outtmpl': str(outpath) + '/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'quiet': True,
    }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return 1 # return 1 for success

def download_channel(n_vids, video_urls, outpath):
    print("Downloading videos...")
    # get max n_vids from channel
    max_attempts = len(video_urls)

    # set download and attempt counters
    n_downloads = 0
    n_attempt = 0  

    # download videos
    while n_downloads < n_vids and n_attempt < max_attempts:
        url = video_urls[n_attempt]
        n_attempt += 1
    
        try:
            success_fail = download_mp4(outpath, url, max_duration=720, min_duration=60)
            n_downloads += success_fail
        
        except:
            print("Error downloading video: ", url)

def transcribe_audio(filename, transcriber, audio_path):
    print("Transcribing audio...")
    file_path = str(audio_path / filename)

    # get audio
    transcript_dict = transcriber(file_path)

    # save dict to file
    text_chunks = transcript_dict['chunks']

    # remove timestamps
    text_chunks = [item["text"] for item in text_chunks]

    print(text_chunks)

    return text_chunks

def main():
    # define paths
    inpath, outpath, audio_path = define_paths()

    # load data from inpath
    data = pd.read_csv(inpath)

    # only keep two random rows (temp)
    data = data.sample(n = 2)

    # initialize models
    transcriber = pipeline('automatic-speech-recognition', 
                           model='openai/whisper-base.en',
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           return_timestamps=True)
    
    # create empty columns for later variables
    data["transcript_chunks"] = None
    data["video_urls"] = None

    # loop through all channels (rows)
    for i, row in data.iterrows():
        # get channel url
        channel_url = row["ha-link"]

        # get channel videos
        video_urls = get_channel_vids(channel_url)

        # download videos
        download_channel(n_vids = 2, video_urls = video_urls, outpath = audio_path)

        # define empty list to store text chunks
        all_text_chunks = []

        # loop through all files in audio_path
        for audio_file in os.listdir(audio_path):
            # transcribe audio
            text_chunks = transcribe_audio(audio_file, transcriber, audio_path)

            # clean transcript
            text_chunks_cln = clean_text(text_chunks)

            # append all elements in text_chunks_cln to all_text_chunks
            all_text_chunks.extend(text_chunks_cln)

            # delete audio file
            os.remove(audio_path / audio_file)
        
        # shuffle list
        random.shuffle(all_text_chunks)

        # append to dataframe
        data.at[i, "video_urls"] = video_urls
        data.at[i, "transcript_chunks"] = all_text_chunks

    # save dataframe to outpath
    data.to_csv(outpath / "top-youtubers-transcribed.csv")

if __name__ == "__main__":
    main()