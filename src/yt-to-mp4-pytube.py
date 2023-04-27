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

    # get 5 most recent videos
    video_urls = channel.video_urls[:10]

    return video_urls

def download_mp4(outpath, url, max_duration):
    # create yt object
    yt = pytube.YouTube(url)

    # check duration and name
    duration = yt.length
    name = yt.title

    # if duration is too long, skip
    if duration > max_duration:
        raise ValueError("Video too long, skipping to next..." + url)
    
    # else download
    else:
        # filter stream for audio only
        stream = yt.streams.filter(only_audio=True)[0]
        # download
        stream.download(filename="{}.mp3".format(name), output_path=outpath)
    


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
            download_mp4(outpath, url, max_duration = 720)
            n_downloads += 1

        except:
            print("Error downloading video: ", url)

def main():
    input_channel = "https://www.youtube.com/user/speedyw03"

    path = Path(__file__)
    outpath = path.parents[1] / "out"

    # get channel videos
    video_urls = get_channel_vids(input_channel)

    # download videos
    download_channel(n_vids = 3, video_urls = video_urls, outpath = outpath)


#if __name__ == "__main__":
    #<main()

# define channel
channel = Channel("https://www.youtube.com/channel/UCci2c90HJbY0VAS3_eLF3Wg/videos")

video_urls = channel.video_urls[:10]

print(video_urls)
