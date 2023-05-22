# Assignment 5 (Self-Assigned): The SafeTuber Pipeline
![safetuber-pipeline (1)](https://github.com/drasbaek/SafeTuber/assets/80207895/9ed95ac7-650d-412b-aa45-e2ecab0fc715)


## Repository Overview
1. [Description & Motivation](#description)
2. [Repository Tree](#tree)
3. [Setup](#setup)
5. [Usage](#usage)
6. [Results](#results)
8. [Discussion & Limitations](#discussion)

## Description & Motivation <a name="description"></a>
This repository forms the solution to self-chosen assignment 5 by *Anton Drasbæk Schiønning (202008161)* in the course "Language Analytics" at Aarhus University. <br>

The **SafeTuber** pipeline is an innovative tool designed to quantify the extent of toxic speech used by top YouTubers. It leverages multiple [Huggingface pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines) to transform speech to text and classify toxicity levels. Based on a ranking of the most popular YouTube channels by [HypeAuditor](https://hypeauditor.com/top-youtube-all-united-states/), I have used the pipeline on a curated top 100 list of the most watched YouTube channels in the United States that are not music artists (e.g. Justin Bieber) or mainstream company channels (e.g. Netflix).

The motivation behind this project is to bridge the generational gap in understanding internet culture. With children spending significant amounts of time consuming YouTube content, parents who didn't grow up with the internet often struggle to assess which content creators are child-friendly and which are not. The **SafeTuber** analysis of 100 channels, along with the ability to analyze any provided channel, serves as a valuable tool to assist parents in navigating this challenging process.

**DISCLAIMER**: *The pipeline worked as of May 31st, 2023. As it is sensitive to changes in YouTube's API, certain functions may break over time, relying on updates from the Python package [`yt_dlp`](https://github.com/yt-dlp/yt-dlp). Bugs will most likely pertain to `get_channel_vids()` and `download_wav()` functions in `transcriber.py`*.

## Repository Tree <a name="tree"></a>
```
├── README.md                       
├── channel_reqs.md            <----- channel requirements for working in the pipeline
├── data
│   ├── top-youtubers-raw.csv           <----- raw file of the top 100 selected YouTubers
│   └── top-youtubers-transcribed.csv
├── out
│   ├── most-toxic-channels.png
│   ├── share-of-toxic-channels.png
│   ├── top-youtubers-classified.csv   <----- detailed output with transcriptions and classifications for top 100
│   └── toxicity-by-category.png
├── requirements.txt
├── setup_linux.sh
├── setup_mac.sh
└── src
    ├── classifier.py                  <----- classify all top 100 YouTube Channels
    ├── single_classify.py             <----- transcribe and classify a single, new YouTube channel
    ├── transcriber.py                 <----- transcribe all top 100 YouTube Channels
    ├── utils.py
    └── visualizations.py              <----- visualize of results in out directory
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
By default, the transcription is done using [*whisper-base.en*](https://huggingface.co/openai/whisper-base.en), although other whisper models listed on [Huggingface](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&sort=downloads) are also compatible for either speeding up the process or making transcriptions better. <br/><br/>
The model, along with the number of videos to analyze per channel (default: 3 videos), can be specified with arguments as such:
```
# uses whisper small to transcribe, analyzes 5 videos per channel
python src/transcriber.py --model "openai/whisper-small" --n_vids 5
```
<br>

Based on the transcriptions, classifications can be completed. The classifier used is [*martin-ha/toxic-comment-model*](https://huggingface.co/martin-ha/toxic-comment-model), a [*DistilBERT*](https://huggingface.co/docs/transformers/model_doc/distilbert) model fine-tuned for toxic commment classificaiton. Classifications are executed as such:
```
python src/classifier.py
```
The results are saved to the `out` directory as `top-youtubers-classified.csv`.
<br/><br/>

### Analyze a New Channel
It is also possible to run the analysis for a new channel that is not on the top 100 list using `single_classify.py`. Please note that channels must conform with requirements specified in `channel_reqs.md` in order for the analysis to be possible. <br>

To do analysis, first obtain the channel's url. In addition, you can also specify `--model` and `--n_vids` arguments for this analysis:
```
# analyze Jake Paul based on 5 videos and transcribe using Whisper (base.en)
python src/single_classify.py --url "https://www.youtube.com/@jakepaul" --n_vids 5 --model "openai/whisper-base.en" 
```
<br>

You will see a result for the channel printed to the terminal, such as:
```
Total number of comments analyzed: 216
Number of toxic comments: 25
Percentage of toxic comments: 0.1157
    
Here is an example of a toxic comment from the channel:
"Bro, nothing. You're literally worthless. You lost a punching battle."
```


## Results (Top 100 channels) <a name="results"></a>
The following results are based on videos analyzed the 7th of May 2023; results will vary if running the analysis again as it will be based on other videos. <br>

From the 100 YouTube Channels, **22,316 transcript comments/chunks from 300 different videos were classified**, 3.6% of which were deemed to be toxic (796 toxic comments/chunks). The visualizations below were created using `visualizations.py` and can also be found in the `out` directory along with `top-youtubers-classified.csv` which contains the raw output data. <br>

### Toxicity by Channel (HypeAuditor) Category
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/toxicity-by-category.png?raw=True)

### Share of Completely Non-Toxic Channels
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/share-of-toxic-channels.png?raw=True)

### Top 10 most Toxic channels compared to Average
![alt text](https://github.com/drasbaek/SafeTuber/blob/main/out/most-toxic-channels.png?raw=True)

## Discussion & Limitations <a name="discussion"></a>
Overall, the results show that only 14% of the channels made no toxic comments across three videos, despite the fact that we **only** analyzed videos without age restrictions. However, the toxicity levels were astoundingly different across the channel categories. Whereas categories such as *Animals & Pets* and *Mystery* showed no toxic content, *Animation* channels had 7% toxic comments on average. *Daily vlogs* and *fitness* follows close after *Animation* as the second and third most toxic channel categories. <br>

In terms of the most toxic channels, the Fortnite icon [Ninja](https://www.youtube.com/channel/UCAW-NpUFkMyCNrvRSSGIvDQ) comes in at first with almost 30 percent of all comments uttered being toxic. The commentary channel [penguinz0](https://www.youtube.com/@penguinz0) joins Ninja as the only other channel with over 20 percent of comments being toxic. <br>

Still, these results should only be interpreted with respect to some major limitations for the analysis:
* As a product of language analytics, the **SafeTuber** pipeline only examines YouTube channels based on the audio modality, ignoring all potentially toxic visual elements in videos.
* `martin-ha/toxic-comment-model` has not been fine-tuned for classifying YouTuber utterances specifically and may thus make misclassifications. A closer inspection of the results also reveals that it classifies YouTubers who swear as very toxic which could be debated. 
* Channels are only analyzed in terms of their most recent videos which may not be representative for the channel as a whole.
* There is a great disparity in the amount of speech analyzed across channels in the analysis due to variation in normal video lengths. <br>

Nevertheless, the Safetuber pipeline offers a framework for assessing toxicity on YouTube based on objective criteria, thereby helping to narrow the parental knowledge gap regarding child-friendly and inappropriate content creators.

Moreover, this project serves as a demonstration of how language analytics can transcend the realm of textual databases. By utilizing sophisticated transcription tools, speech audio files can be properly analyzed, expanding the application of language analytics in analyzing different forms of media.





