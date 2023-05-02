# load packages
from pytube import Channel
import pytube
from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm
from moviepy.editor import *
from transformers import pipeline
import torch
from utils import *
import pandas as pd
import os
import random

def define_paths():
    # define path
    path = Path(__file__)

    # define inpath
    inpath = path.parents[1] / "data"

    # define outpath
    outpath = path.parents[1] / "out"

    # define path to temporary audio storage
    audio_path = path.parents[1] / "audio_files"

    return inpath, outpath, audio_path


def initialize_models():
    # define device to use
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # initialize transcriber
    transcriber = pipeline('automatic-speech-recognition', 
                           model='openai/whisper-base.en',
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           return_timestamps=True,
                           device = device)
    # initialize classifier
    classifier = pipeline("text-classification", 
                          model = "martin-ha/toxic-comment-model")

    return transcriber, classifier

def get_channel_vids(channel_url):
    # define channel
    channel = Channel(channel_url)

    # get up to the first 100 video urls (if there are that many)
    try:
        video_urls = channel.video_urls[:100]
    except:
        video_urls = channel.video_urls

    return video_urls

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

def classify_transcript(text_chunks, classifier):
    print("Classifying text chunks...")
    """
    Classify text chunks as toxic or not toxic.
    """
    # initialize empty list to store classifications
    classifications = []

    # loop over text chunks with tqdm
    for text_chunk in text_chunks:
        # classify text chunk
        classification = classifier(text_chunk)[0]

        # append classification label to list
        classifications.append(classification["label"])

    return classifications

def toxicity_aggregates(text_chunks, classifications):
    """
    Calculate toxicity aggregates.
    """
    # calculate percentage of toxic comments
    n_toxic = classifications.count("toxic")
    n_comments = len(classifications)

    # get a toxic comment if there is one
    if n_toxic != 0:
        pct_toxic = n_toxic / n_comments
        # get all toxic comments
        toxic_comments = [text_chunks[i] for i in range(len(text_chunks)) if classifications[i] == "toxic"]
    else:
        toxic_comments = None
        pct_toxic = 0

    return pct_toxic, toxic_comments

def main():
    # define paths
    inpath, outpath, audio_path = define_paths()

    # load data from inpath
    data = pd.read_csv(inpath / "top-youtubers.csv")

    # only keep two random rows (temp)
    data = data.sample(n = 5)

    # create empty columns for later variables
    data["transcript_chunks"] = None
    data["pct_toxic"] = None
    data["toxic_comments"] = None

    # initialize models
    transcriber, classifier = initialize_models()

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

        # classify text chunks
        classifications = classify_transcript(all_text_chunks, classifier)

        # calculate toxicity aggregates
        pct_toxic, toxic_comments = toxicity_aggregates(all_text_chunks, classifications)

        # append to dataframe
        data.at[i, "transcript_chunks"] = all_text_chunks
        data.at[i, "toxic_comments"] = toxic_comments
        data.loc[i, "pct_toxic"] = pct_toxic

    # save dataframe to outpath
    data.to_csv(outpath / "top-youtubers-with-classifications.csv")


if __name__ == "__main__":
    main()









