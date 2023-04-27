from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import pipeline
from scipy.io import wavfile

samplerate, audio = wavfile.read('./out/The BEST of CREW MEMES!.wav')

transcriber = pipeline('automatic-speech-recognition', model='openai/whisper-tiny.en')

test = transcriber('audio.wav')

print(test)
