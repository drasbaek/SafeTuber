import pandas
from mp3_to_text import *
from yt_to_mp3 import *
import tqdm

path = Path(__file__)
audio_path = path.parents[1] / "audio_files"

# load in the data
data = pandas.read_csv("data/top-youtubers.csv")

# only keep first 100 rows
data = data.iloc[:2]

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

    for audio in os.listdir(audio_path):
        text_chunks = transcribe_audio(audio, transcriber)
        text_chunks_cln = clean_text(text_chunks)

        # save to file in out folder
        with open("out/" + audio + ".txt", "w") as f:
            for chunk in text_chunks_cln:
                f.write(chunk + "\n")
    
    # delete audio files
    for audio in os.listdir(audio_path):
        os.remove(audio_path / audio)



