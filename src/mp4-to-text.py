from transformers import pipeline
import torch
import re
import json

def initialize_transcriber():
    # define device to use
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # initialize transcriber
    transcriber = pipeline('automatic-speech-recognition', 
                           model='openai/whisper-base.en',
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           return_timestamps=True,
                           device = device)
    return transcriber

def transcribe_audio(filename, transcriber):
    file_path = "./out/" + filename

    # get audio
    transcript_dict = transcriber(file_path)

    # save dict to file
    text_chunks = transcript_dict['chunks']

    # remove timestamps
    text_chunks = [item["text"] for item in text_chunks]

    return text_chunks


def remove_duplicates(text_chunks):
    # initialize new list
    new_text_chunks = []

    # initialize previous text
    prev_text = ""

    # loop through chunks
    for text in text_chunks:

        # if text is the same as previous text, skip
        if text == prev_text:
            continue

        # else add to new list
        else:
            new_text_chunks.append(text)
            prev_text = text

    return new_text_chunks

def concatenate_chunks(text_chunks):
    joined_chunks = []
    current_string = ""

    for i, string in enumerate(text_chunks):
        
        # Join current string with next string if current string is too short
        if len(current_string.split()) < 10:
            current_string += " " + string
        
        # Add current string to joined data if it's long enough
        else:
            joined_chunks.append(current_string.strip())
            current_string = string

        # Add the last string to the joined data
        if i == len(text_chunks) - 1:
            joined_chunks.append(current_string.strip())
    
    return joined_chunks


def main():
    '''
    transcriber = initialize_transcriber()
    filename = "MORE NEW TRACKS!! THIS THE BEST WAVE SO FAR!! [MK8D].wav"
    text_chunks = transcribe_audio(filename, transcriber)
    '''
    
    # read dict from json
    with open("transcript.json", "r") as f:
        text_chunks = json.load(f)
    
    # remove duplicates
    text_chunks_1 = remove_duplicates(text_chunks)

    # concatenate chunks
    text_chunks_2 = concatenate_chunks(text_chunks_1)

    print(len(text_chunks_2))

    # write dict to json
    with open("transcript_clean.json", "w") as f:
         json.dump(text_chunks_2, f)
    

if __name__ == "__main__":
    main()