# Assignment 5 (Self-Assigned): The SafeTuber Pipeline
![safetuber-pipeline](https://github.com/drasbaek/SafeTuber/assets/80207895/374530af-180f-4329-9fc4-208b62c5b507)


## Repository Overview
1. [Description & Motivation](#description)
2. [Repository Tree](#tree)
3. [Setup](#setup)
5. [Usage](gusage)
6. [Results](#results)
8. [Discussion & Limitations](#discussion)

## Description & Motivation <a name="description"></a>
This repository forms the solution to self-chosen assignment 5 by Anton Drasbæk Schiønning (202008161) in the course "Language Analytics" at Aarhus University. <br>

The **SafeTuber** pipeline is a tool that quantifies the amount of toxic speech used by the top YouTubers. <br> 

Based on a ranking of the most popular YouTube channels by [HypeAuditor](https://hypeauditor.com/top-youtube-all-united-states/), we have identified and analyzed 100 of the most watched YouTube channels in the United States that are not music artists (e.g. Justin Bieber) or main stream company channels (e.g. Netflix).

The motivation behind this project is to provide a tool which may bridge the generational gap in understanding internet culture. Whereas children spend many hours consuming content on YouTube, it may be a cumbersome task for parents, who did not grown up online, to assess which content creators are child-friendly and who are not. The **SafeTuber** analysis of 100 channels, as well as a tool for analyzing any other provided channel, can help guide parents in this tough process by utilizing multiple language models in a single pipeline.

**DISCLAIMER**: *The pipeline worked as of May 31st, 2023. As it is sensitive to changes in YouTube's API, certain functions may break over time and rely on updates from the package [`yt_dlp`](https://github.com/yt-dlp/yt-dlp). Bugs will most likely pertain to `get_channel_vids()` and `download_mp3()` functions in `transcriber.py`*.

## Repository Tree <a name="tree"></a>
```
├── README.md                       
├── channel_reqs.md                    <----- YT Channel requirements for functioning in the pipeline
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

## Setup <a name="setup"></a>
**NB:** *This setup will use **brew** or **sudo** to install ffmpeg to your device. This is necessary for replicating the analysis.* 
<br>
<br>
To replicate the analysis, you must have Python3 installed and run the setup file. The setup file varies between MacOS and Linux, as these operating systems differ in their way to install [ffmpeg](https://ffmpeg.org/) which is required for the analysis. <br>

To install requirements, create a virtual environment and install ffmpeg, run the following from the root directory
```
bash setup_mac.sh     # for MacOS users
bash setup_linux.sh   # for Linux users
```

## Usage <a name="usage"></a>
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

### Analyze a New Channel
It is also possible to run the analysis for a new channel that is not on the pre-spcecified list using `single_classify.py`. Please note that channels must confirm with requirements specified in `channel_reqs.md` in order for the analysis to be possible. <br>

To do analysis, first obtain the channel's url. In addition, you can also specify `--model` and `--n_vids` arguments for this analysis:
```
# analyze Jake Paul based on 5 videos and transcribe using Whisper (base.en)
python src/single_classify.py --url "https://www.youtube.com/@jakepaul" --n_vids 5 --model "openai/whisper-base.en" 
```

You will see a result for the channel printed to the terminal, such as:
```
Total number of comments analyzed: 216
Number of toxic comments: 25
Percentage of toxic comments: 0.1157
    
Here is an example of a toxic comment from the channel:
"Shout out to Floyd. Hey Floyd, download Betr and maybe you can earn enough money to pay back my brother, you scumbag."
```


## Results (Top 100 channels) <a name="results"></a>
Overall, **22,316 transcript comments/chunks from 300 different videos were classified**, 3.6% of which were deemed to be toxic (796 toxic comments/chunks).

The visualizations below were created using `visualizations.py` and can also be found in the `out` directory along with `top-youtubers-classified.csv` which contains the raw output data. <br>

These results are based on videos analyzed the 7th of May 2023, results will vary if running the analysis again as it will be based on other videos.

### Toxicity by Channel (HypeAuditor) Category
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/toxicity-by-category.png?raw=True)

### Share of Completely Non-Toxic Channels
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/share-of-toxic-channels.png?raw=True)

### Top 10 most Toxic channels compared to Average
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/most-toxic-channels.png?raw=True)

## Discussion & Limitations <a name="discussion"></a>
Overall, the results show that only 14% of the channels made no toxic comments across 3 videos, despite the fact that we only analyzed videos without age-restrictions. The results were astoundingly different across the channel categories. Whereas categories such as *Animals & Pets* and *Mystery* showed no toxic content, an *Animation* channels had 7% toxic comments on average. *Daily vlogs* and *fitness* follows close after as the second and third most toxic channel categories. <br>

In terms of the most toxic channels, Fornite icon Ninja comes in at first with almost 30 percent of all comments uttered being toxic. penguinz0 joins Ninja as the only other channel with over 20% of comments being toxic. <br>

Some of the central limitations of this project and its results should be addressed:
* It only looks at YouTube channels based on the audio modality, ignoring all potentially toxic visual elements in videos.
* Channels are only analyzed in terms of their most recent videos and there are great discrepancies in the amount of transcript analyzed across channels due to variation in normal video lengths. <br>
* `martin-ha/toxic-comment-model` has not been fine-tuned for classifying YouTuber utterances specifically and may thus make misclassifications. A closer inspection of the results also reveals that it classifies YouTubers who swear as very toxic which could be debated.

Despite all of this, the Safetubers pipeline provides forms a skeleton for analyzing toxicity on YouTube using objective criteria, contributing to enhancing parental understanding of how all internet personalities may not be equally child-friendly.





