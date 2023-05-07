""" classifier.py
Author: 
    Anton Drasbæk Schiønning (202008161), GitHub: @drasbaek

Desc:
    Classifies transcripts from YouTube channels in chunks as either toxic or not toxic.
    It utilizes a toxicity classification model from HuggingFace's model hub (https://huggingface.co/martin-ha/toxic-comment-model).
    The model is a fine-tuned version of the DistilBERT model for toxicity classification (https://huggingface.co/distilbert-base-uncased).

    Hence, this file covers the last two steps in the SafeTuber pipeline:
        6. Classifying toxicity in chunks
        7. Calculating average toxicity level for a channel

    This script analyzes all the 200 channels in the top-youtubers-transcribed.csv file and provides transcriptions of their recent
    videos in out/top-youtubers-classified.csv.

Usage:
    $ python src/classifier.py
"""


from pathlib import Path
from transformers import pipeline
import pandas as pd
from tqdm import tqdm

def define_paths():
    # define path
    path = Path(__file__)

    # define inpath
    inpath = path.parents[1] / "data"

    # define outpath
    outpath = path.parents[1] / "out"

    return inpath, outpath


def classify_transcript(text_chunks, classifier):
    """
    Classify text chunks as toxic or not toxic.
    """

    # initialize empty list to store classifications
    classifications = []

    # loop over text chunks with tqdm
    for text_chunk in text_chunks:
        # classify text chunk
        classification = classifier(text_chunk)[0]

        # append classification label to list
        classifications.append(classification["label"])

    return classifications

def toxicity_aggregates(text_chunks, classifications):
    """
    Calculate toxicity aggregates.
    """
    # calculate percentage of toxic comments
    n_toxic = classifications.count("toxic")
    n_comments = len(classifications)

    # get a toxic comment if there is one
    if n_toxic != 0:
        # calculate percentage of toxic comments
        pct_toxic = round(float(n_toxic) / float(n_comments), 3)
        
        # get all toxic comments
        toxic_comments = [text_chunks[i] for i in range(len(text_chunks)) if classifications[i] == "toxic"]
        
        # change toxic commments to a string
        toxic_comments = str(toxic_comments)
    
    else:
        toxic_comments = None
        pct_toxic = 0

    return n_comments, n_toxic, pct_toxic, toxic_comments

def main():
    print("Classifying text chunks...")
    # define paths
    inpath, outpath = define_paths()

    # load data from inpath
    data = pd.read_csv(inpath / "top-youtubers-transcribed.csv")

    # change data type of transcript_chunks to list
    data["transcript_chunks"] = data["transcript_chunks"].apply(lambda x: eval(x))

    # initialize classifier
    classifier = pipeline("text-classification", 
                          model = "martin-ha/toxic-comment-model")
    # loop with tqdm
    for i, row in tqdm(data.iterrows(), total = len(data)):
        # get transcript chunks
        transcript_chunks = row["transcript_chunks"]

        # classify transcript chunks
        classifications = classify_transcript(transcript_chunks, classifier)

        # calculate toxicity aggregates
        n_comments, n_toxic, pct_toxic, toxic_comments = toxicity_aggregates(transcript_chunks, classifications)
        
        # save data
        data.loc[i, "n_comments"] = n_comments
        data.loc[i, "n_toxic"] = n_toxic
        data.loc[i, "pct_toxic"] = pct_toxic
        data.loc[i, "toxic_comments"] = toxic_comments

    # save data
    #data.to_csv(outpath / "top-youtubers-classified.csv", index = False)
    data.to_csv(outpath / "top-youtubers-classified.csv", index = False)


if __name__ == "__main__":
    main()