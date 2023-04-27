from transformers import pipeline
import torch

def initialize_transcriber():
    # define device to use
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # initialize transcriber
    transcriber = pipeline('automatic-speech-recognition', 
                           model='openai/whisper-tiny.en',
                           chunk_length_s = 30, # must be 30 to chunk correctly
                           device = device)
    return transcriber

def transcribe_audio(filename, transcriber):
    file_path = "./out/" + filename

    # get audio
    transcript_dict = transcriber(file_path)

    # save dict to file
    text = transcript_dict['text']

    return text


def main():
    transcriber = initialize_transcriber()
    filename = "Robert ＂Kool＂ Bell on Kool & The Gang Being the Most-Sampled Group, Sampled 1,800 Times (Part 1).wav"
    text = transcribe_audio(filename, transcriber)
    print(text)

if __name__ == "__main__":
    main()