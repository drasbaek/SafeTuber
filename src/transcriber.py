""" transcriber.py
Author: 
    Anton Drasbæk Schiønning (202008161), GitHub: @drasbaek

Desc:
    Transcribes videos from youtube channels based on the channel url.
    It utilizes the youtube-dl library to download the videos and the HuggingFace transformers library to transcribe the audio.
    Specifically, OpenAI's Whisper is used to transcribe the obtained MP3 files.

    Hence, this file covers the first 5 steps in the SafeTuber pipeline:
        1. Identifying YouTube channel
        2. Getting recent video urls
        3. Downloading MP3s
        4. Transcribing audio files
        5. Merging and shuffling transcripts.

    This script analyzes all the 100 channels in the top-youtubers-curated.csv file and provides transcriptions of their recent
    videos in data/top-youtubers-transcribed.csv.

Usage:
    $ python src/transcriber.py --n_vids 4 --model "openai/whisper-medium.en"
"""

# import packages
from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline
from utils import *
import pandas as pd
import os
import random
import io
import sys

def define_paths():
    """
    Define paths to data, output, and temporary audio storage.

    Returns:
        inpath (pathlib.PosixPath): Path to data
        outpath (pathlib.PosixPath): Path to output
        audio_path (pathlib.PosixPath): Path to temporary audio storage
    """

    # define path
    path = Path(__file__)

    # define inpath
    inpath = path.parents[1] / "data" / "top-youtubers-raw.csv"
    
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
    It is necessary to obtain these urls from the terminal output as extract_info does not return those.

    Args:
        channel_url (str): URL of the YouTube channel
    
    Returns:
        urls (list): List of video urls
    """

    # create a StringIO object to capture stdout
    captured_output = io.StringIO()

    # redirect stdout to the StringIO object
    sys.stdout = captured_output

    # define ydl options
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 
                'playlistend': 30,
                'ignoreerrors': True # necessary to skip videos that fail (e.g. due to age or country restrictions)
                }
    
    # download the channel
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(
            channel_url,
            download=False
        )

    # restore stdout to its original value
    sys.stdout = sys.__stdout__

    # get output
    output = captured_output.getvalue()

    # extract all urls from output
    urls = []

    for line in output.splitlines():
        if "https://www.youtube.com/watch?v=" in line:
            
            # extract only the url from the line
            url = line.split(" ")[-1]
            urls.append(url)

    return urls

def download_mp3(outpath, url, max_duration, min_duration):
    """
    Downloads an MP3 file from a YouTube video.
    NOTE: This is immediately deleted after the audio has been transcribed to comply with YouTube's terms of service and save memory.

    Args:
        outpath (pathlib.PosixPath): Path to output
        url (str): URL of the YouTube video
        max_duration (int): Maximum allowed duration of a video in seconds (check channel_reqs.txt for more info)
        min_duration (int): Minimum allowed duration of a video in seconds (check channel_reqs.txt for more info)

    Returns:
        success_fail (int): 1 if the download was successful, 0 if it failed.
    """

    # get info on video
    ydl = YoutubeDL()
    info_dict = ydl.extract_info(url, download=False)

    # check duration
    duration = info_dict.get('duration')

    # if duration is too long, skip
    if duration > 1200:
        print("Video too long, skipping to next..." + url)
        return 0 # return 0 for fail
    
    # if duration is too short, skip
    if duration < 120:
        print("Video too short, skipping to next..." + url)
        return 0 # return 0 for fail

    # else initialize ydl options
    else:
        ydl_opts = {
        'outtmpl': str(outpath) + '/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'ignoreerrors': True , # necessary to skip videos that fail (e.g. due to age or country restrictions)
        'quiet': True, # don't print to stdout
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav'
    }],
        }

        # attempt to download the video
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return 1 # return 1 for success
            except:
                return 0 # return 0 for a failed download


def download_channel(n_vids, video_urls, outpath):
    """
    Uses download_mp3 function to download videos from a channel, the number is determined by n_vids.

    Args:
        n_vids (int): Number of videos to be downloaded
        video_urls (list): List of video urls
        outpath (pathlib.PosixPath): Path to output
    
    Returns:
        used_urls (list): List of urls that were used to download videos
    """

    # get max n_vids from channel based on how many videos are available
    max_attempts = len(video_urls)
    
    # initialize list of used urls
    used_urls = []

    # set download and attempt counters
    n_downloads = 0
    n_attempt = 0  

    # download videos
    while n_downloads < n_vids and n_attempt < max_attempts:
        url = video_urls[n_attempt]
        n_attempt += 1
    
        try:
            success_fail = download_mp3(outpath, url, max_duration=3000, min_duration=120)
            n_downloads += success_fail
        
        except:
            print("Error downloading video: ", url)
        
        # only append url if download was successful
        if success_fail == 1:
            used_urls.append(url)
    
    return used_urls

def transcribe_audio(filename, transcriber, audio_path):
    """
    Transcribes an audio file using the HuggingFace pipeline.
    The transcription is done with timestamps, in order to ensure proper chunking.

    Args:
        filename (str): Name of the audio file
        transcriber (pipeline): HuggingFace pipeline for transcription
        audio_path (Path): Path to audio file storage
    
    Returns:
        text_chunks (list): List of text chunks from the transcription
    """

    # get audio file path
    file_path = str(audio_path / filename)

    # transcribe the audio
    transcript_dict = transcriber(file_path, max_new_tokens = 448)

    # get text chunks
    text_chunks = transcript_dict['chunks']

    # remove timestamps
    text_chunks = [item["text"] for item in text_chunks]

    return text_chunks

def main():
    # define paths
    inpath, outpath, audio_path = define_paths()

    # load data from inpath
    data = pd.read_excel(inpath)

    # initialize models
    transcriber = pipeline('automatic-speech-recognition', 
                           model='openai/whisper-base.en',
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           return_timestamps=True)
    
    # create empty columns for later variables
    data["transcript_chunks"] = None
    data["video_urls"] = None

    # loop through all channels (rows) with tqdm
    print("Downloading videos and transcribing...")
    for i, row in tqdm(data.iterrows(), total = len(data)):
        # get channel url
        channel_url = row["channel_url"]

        # get channel videos
        video_urls = get_channel_vids(channel_url)

        # download videos
        used_urls = download_channel(n_vids = 3, video_urls = video_urls, outpath = audio_path)

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
        data.at[i, "video_urls"] = used_urls
        data.at[i, "transcript_chunks"] = all_text_chunks

    # save dataframe to outpath
    data.to_csv(outpath / "top-youtubers-transcribed.csv")

if __name__ == "__main__":
    main()