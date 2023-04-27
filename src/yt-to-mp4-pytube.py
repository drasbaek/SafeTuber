from pytube import Channel
import pytube
from pathlib import Path

def get_channel_vids(channel_url):
    # define channel
    channel = Channel(channel_url)

    # get 5 most recent videos
    video_urls = channel.video_urls[:10]

    return video_urls

def download_audio(outpath, url, max_duration):
    # create yt object
    yt = pytube.YouTube(url)

    # check duration and name
    duration = yt.length / 60
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
            download_audio(outpath, url, max_duration_minutes = 15)
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
    #main()


# test for single video
url = "https://www.youtube.com/watch?v=2uvV1-02UCU"

yt = pytube.YouTube(url)

stream = yt.streams.filter(only_audio=True)[0]

stream.download()