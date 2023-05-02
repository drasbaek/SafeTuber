import pandas as pd
from mp3_to_text import *
from yt_to_mp3 import *
import tqdm
import random

path = Path(__file__)
audio_path = path.parents[1] / "audio_files"

# load in the data
data = pd.read_csv("data/top-youtubers.csv")

# only keep first 100 rows
data = data.iloc[:2]

# create empty column for text chunks that is object type
data["text_chunks"] = ""

print(data)

# initialize transcriber
transcriber = initialize_transcriber()

# loop over rows with tqdm
for index, row in tqdm.tqdm(data.iterrows(), total = data.shape[0]):
    # identify channel url
    url = row["ha-link"]

    # get channel videos
    video_urls = get_channel_vids(url)

    # download videos
    download_channel(n_vids = 2, video_urls = video_urls, outpath = audio_path)

    # define empty list to store text chunks
    all_text_chunks = []

    for audio in os.listdir(audio_path):
        text_chunks = transcribe_audio(audio, transcriber)
        text_chunks_cln = clean_text(text_chunks)
        all_text_chunks.append(text_chunks_cln)

        # delete audio file
        os.remove(audio_path / audio)
    
    # delete audio files
    for audio in os.listdir(audio_path):
        os.remove(audio_path / audio)

    # shuffle text chunks
    all_text_chunks = random.shuffle(all_text_chunks)

    # save text chunks to dataframe
    data.at[index, "text_chunks"] = all_text_chunks

# write to a new csv
data.to_csv("data/top-youtubers-with-text.csv", index = False)




