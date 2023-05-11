# Assignment 5 (Self-Assigned): The SafeTuber Project
![copy-test](https://user-images.githubusercontent.com/80207895/236698306-3499d444-c791-497b-a10b-2b6a7b087e9c.png)


## Description
This repository forms the solution to self-chosen assignment 5 by Anton Drasbæk Schiønning (202008161) in the course "Language Analytics" at Aarhus University. <br>

The "SafeTubers" pipeline is a tool that quantifies the amount of toxic speech used by the top YouTubers. <br> 

Based on a ranking of the most popular YouTube channels by [HypeAuditor](https://hypeauditor.com/top-youtube/), we have identified and analyzed 100 of the most watched YouTube channels in the United States that are not music artists (e.g. Justin Bieber) or main stream company channels (e.g. Netflix).

The motivation behind this project is to provide a tool which may bridge the generational gap in understanding internet culture. Whereas children spend many hours consuming content on YouTube, it may be a cumbersome task for parents to assess which content creators are child-friendly and who are not. "Safetubers" analysis of 100 channels, as well as a tool for analyzing any other provided channel, can help guide parents in this tough process by combining utilizing multiple language models in a single pipeline.

## Repository Tree
```
├── README.md                       
├── channel_reqs.txt                    <----- YT Channel requirements for functioning in the pipeline
├── data
│   ├── top-youtubers-raw.csv           <----- Raw file of the top 100 selected YouTubers
│   └── top-youtubers-transcribed.csv
├── out
│   ├── most-toxic-channels.png
│   ├── share-of-toxic-channels.png
│   ├── top-youtubers-classified.csv   <----- Detailed output with transcriptions and classificationsf for top 100
│   └── toxicity-by-category.png
├── requirements.txt
├── setup_linux.sh
├── setup_mac.sh
└── src
    ├── classifier.py                  <----- Classification of all top 100 YouTube Channels
    ├── single_classify.py             <----- Transcription and classification of single, new YouTube channel
    ├── transcriber.py                 <----- Transcription of all top 100 YouTube Channels
    ├── utils.py
    └── visualizations.py              <----- Visualizations of results in out directory
```

## Setup
To replicate the analysis, you must have Python3 installed and run the setup file. The setup file varies between MacOS and Linux, as these operating systems differ in their way to install [ffmpeg](https://ffmpeg.org/) which is required for the analysis. <br>

To install requirements, create a virtual environment and install ffmpeg, run the following from the root directory
```
bash setup_mac.sh     # for MacOS users
bash setup_linux.sh   # for Linux users
```

## Usage
### Running the Analysis (Top 100 channels)
To run the analysis, you must first run `transcriber.py` which obtains video urls, extracts audio files, transcribes them and merges it into chunks for each channel:
```
python src/transcriber.py
```
By default, the transcription is done using whisper-base.en, although other whisper models listed on [Huggingface](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=downloads) are also compatible for either speeding up the process or making transcriptions better. <br/><br/>
These, along with the number of videos to analyze per channel (default is 3), can be specified with flags as such:
```
python src/transcriber.py --model "openai/whisper-small" --n_vids 5     # uses whisper small to transcribe, analyzes 5 videos per channel
```

Based on the transcriptions, classification can be completed with `classifier.py`:
```
python src/classifier.py
```
The results are saved to the `out` directory as `top-youtubers-classified.csv`.
<br/><br/>

### Run analysis for new Channel
It is also possible to run the analysis for a new channel that you wish to investigate from its url. The `--model` and `--n_vids` arguments can also be specified here, for example:
```
python src/transcribe_classify_new.py --url "https://www.youtube.com/@cognitivescienceclubatucda6837" --model "openai/whisper-base.en" --n_vids 3
```
Results will be printed to the terminal. <br>
Please note that channels must confirm with requirements specified in `channel_reqs.txt` in order for the analysis to be possible.

## Results
Overall, **22,316 transcript chunks from 300 different videos were classified**, 3.6% of which were deemed to be toxic (796 toxic chunks).

The visualizations below were created using `visualize_results.py` and can also be found in the `out` directory along with `top-youtubers-classified.csv` which contains the raw output data. <br>

These results are based on videos analyzed the 7th of May 2023, results will vary if running the analysis again as it will be based on other videos.

### Toxicity by Channel (HypeAuditor) Category
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/toxicity-by-category.png?raw=True)

### Share of Completely Non-Toxic Channels
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/share-of-toxic-channels.png?raw=True)

### Top 10 most Toxic channels compared to Average
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/most-toxic-channels.png?raw=True)

## Limitations
Some of the central limitations of this project should be addressed. <br/><br/>
Firstly, it only looks at YouTube channels based on the audio modality, ignoring all potentially toxic visual elements in videos. <br>
Also, channels are only analyzed in terms of their most recent videos and there are great discrepancies in the amount of transcript analyzed across channels due to variation in normal video lengths. <br>
Finally, `martin-ha/toxic-comment-model` has not been fine-tuned for classifying YouTuber utterances specifically and may thus make misclassifications as a closer inspection of the results also will reveal. <br>

Despite all of this, the Safetubers pipeline provides forms a skeleton for analyzing toxicity on YouTube using objective criteria, contributing to enhancing parental understanding of how all internet personalities may not be equally child-friendly.





