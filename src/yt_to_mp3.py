from pytube import Channel
import pytube
from yt_dlp import YoutubeDL
from pathlib import Path
from tqdm import tqdm
from moviepy.editor import *
import os
import subprocess

def get_channel_vids(channel_url):
    # define channel
    channel = Channel(channel_url)

    # get 50 most recent videos
    video_urls = channel.video_urls[1:50]

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
    
    if duration < 60:
        print("Video too short, skipping to next..." + url)
        return 0

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

def main():
    input_channel = "https://www.youtube.com/channel/UCERUmrDh9hmqEXBsnYFNTIA"

    path = Path(__file__)
    outpath = path.parents[1] / "out"

    # get channel videos
    video_urls = get_channel_vids(input_channel)

    # download videos
    download_channel(n_vids = 2, video_urls = video_urls, outpath = outpath)

if __name__ == "__main__":
    main()







