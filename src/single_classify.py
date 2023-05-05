""" single_classify.py
Utilizes functions from the transcriper.py and classifier.py to setup a pipeline for new channel classifications.
Channels provided for this analysis must conform with requirements specified in channel_reqs.txt.

"""

from transcriber import *
from classifier import *
from utils import *
import argparse

def arg_parse():
    '''
    Parse command line arguments.
    Returns:
    -   args (argparse.Namespace): Parsed arguments.
    '''
    
    # define parser
    parser = argparse.ArgumentParser(description='Classify toxicity of YouTube Channel')

    # add arguments
    parser.add_argument('-n', '--n_vids', default=4, type=int, help='Number of videos to be analyzed')
    parser.add_argument('-m', '--model', default="openai/whisper-medium.en", help='Model to be used for transcription')
    parser.add_argument('-u', '--url', default='https://www.youtube.com/channel/UCuAXFkgsw1L7xaCfnd5JJOw', help='YouTube URL of channel')

    # parse arguments
    args = parser.parse_args()

    return args


def initialize_models(args):
    transcriber = pipeline('automatic-speech-recognition', 
                           model=args.model,
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           return_timestamps=True)
    
    classifier = pipeline("text-classification", 
                          model = "martin-ha/toxic-comment-model")

    return transcriber, classifier

def create_audio_path():
    # define path
    path = Path(__file__)

    # create dir for audio files if it doesn't exist
    if not os.path.exists(path.parents[1] / "audio_files"):
        os.makedirs(path.parents[1] / "audio_files")
    
    # define path to temporary audio storage
    audio_path = path.parents[1] / "audio_files"

    return audio_path


def toxicity_output(all_text_chunks, classifications):
    """
    Calculate toxicity aggregates.
    """
    # calculate percentage of toxic comments
    n_toxic = classifications.count("toxic")
    n_comments = len(classifications)

    # get a toxic comment if there is one
    if n_toxic != 0:
        # calculate percentage of toxic comments
        pct_toxic = round(float(n_toxic) / float(n_comments), 4)
        
        # get all toxic comments
        toxic_comments = [all_text_chunks[i] for i in range(len(all_text_chunks)) if classifications[i] == "toxic"]

        # create toxic output
        toxic_output = f'''
        Here is an example of a toxic comment from the channel:
        "{toxic_comments[0]}"
        '''
    
    else:
        toxic_comments = None
        pct_toxic = 0
        toxic_output = ""
    
    # format output
    main_output = f'''
    Total number of comments analyzed: {n_comments}
    Number of toxic comments: {n_toxic}
    Percentage of toxic comments: {pct_toxic}
    '''

    return main_output, toxic_output


def main():
    args = arg_parse()

    print(f"(1/7) Identifying toxicity levels for {args.url}")

    # create audio path
    audio_path = create_audio_path()

    # get channel videos
    print("(2/7) Getting video urls...")
    video_urls = get_channel_vids(args.url)

    # download videos
    print("(3/7) Downloading MP3s...")
    used_urls = download_channel(n_vids = args.n_vids, video_urls = video_urls, outpath = audio_path)

    # initialize transcriber and classifier
    print("(4/7) Initialize models and transcribe audio...")
    transcriber, classifier = initialize_models(args)

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
    print("(5/7) Merging and shuffling transcript...")
    random.shuffle(all_text_chunks)

    # classify transcript chunks
    print("(6/7) Classifying transcript chunks...")
    classifications = classify_transcript(all_text_chunks, classifier)

    # calculate toxicity aggregates
    print("(7/7) Calculating aggregates...")
    main_output, toxic_output = toxicity_output(all_text_chunks, classifications)
    

    # print output
    print(main_output)
    print(toxic_output)

if __name__ in "__main__":
    main()