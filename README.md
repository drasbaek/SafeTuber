# Assignment 5 (Self-Assigned): The SafeTuber Project
<img width="1551" alt="Screenshot 2023-05-04 at 15 03 03" src="https://user-images.githubusercontent.com/80207895/236212819-b9fd96a1-86c1-4ec6-b5d2-60d6407b39d6.png">

## Description
This repository forms the solution to self-chosen assignment 5 by Anton Drasbæk Schiønning (202008161) in the course "Language Analytics" at Aarhus University. <br>

The "SafeTubers" project sets out to quantify the amount of toxic speech used by the top YouTubers in the United States. <br> 

Based on a ranking of the most popular YouTube channels by [HypeAuditor](https://hypeauditor.com/top-youtube/), we have identified and analyzed 200 of the most watched YouTube channels in the United States that are not music artists (e.g. Justin Bieber) or main stream company channels (e.g. Netflix). That is, this project focuses on which content creators on YouTube that produce the most toxic content in terms of their utterances. <br>

The motivation behind this project is to provide a tool which may bridge the generational gap in understanding internet culture. Whereas children spend many hours consuming content on YouTube, it may be a cumbersome task for parents to assess which content creators are child-friendly and who are not. "Safetubers" analysis of 200 channels, as well as a tool for analyzing any other provided channel, can help guide parents in this tough process.

## Setup
To replicate the analysis, you must have Python3 installed and run the setup file. The setup file varies between MacOS and Linux, as these operating systems vary in their way to install [ffmpeg](https://ffmpeg.org/) which is required for the analysis (please download ffmpeg manually and install requirements if using Windows). <br>

To install requirements, create a virtual environment and install ffmpeg, run the following from the root directory
```
bash setup_mac.sh     # for MacOS users
bash setup_linux.sh   # for Linux users
```
## Usage
### Running the Analysis (Top 200 channels)
To run the analysis, you must first run `transcriber.py` which obtains video urls, extracts audio files, transcribes them and merges it into chunks for each channel:
```
python src/transcriber.py
```
By default, the transcription is done using whisper-base.en, although other whisper models listed on [Huggingface](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=downloads) are also compatible for either speeding up the process or making transcriptions better. <br/><br/>
These, along with the number of videos to analyze per channel (default is 4), can be specified with flags as such:
```
python src/transcriber.py --model "openai/whisper-small" --n_vids 5     # uses whisper small to transcribe, analyzes 5 videos per channel
```

Based on the transcriptions, classification can be completed with `classifier.py`:
```
python src/classifier.py
```
The results are saved to the `out` directory as `top-youtubers-classified.csv`


### Run analysis for new Channel
It is also possible to run the analysis for a new channel that you wish to investigate from its url. The `--model` and `n_vids` arguments can also be specified here, for example:
```
python src/transcribe_classify_new.py --url "https://www.youtube.com/@cognitivescienceclubatucda6837" --model "openai/whisper-base.en" --n_vids 3
```
Results will be printed to the terminal <br>.
Please note that channels must confirm with requirements specified in `channel_requirements.txt` in order for the analysis to be possible.

## Results
The visualizations below were created using `visualize_results.py` and can also be found in the `out` directory:

## Discussion of Results

## Disclaimer








