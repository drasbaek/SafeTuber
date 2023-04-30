from transformers import pipeline
import pandas as pd
import tqdm

# load data with transcripts
data = pd.read_csv("data/top-youtubers-with-text.csv")

# change text chunks to list
data["text_chunks"] = data["text_chunks"].apply(eval)

# load toxicity classifier
classifier = pipeline("text-classification", model = "martin-ha/toxic-comment-model")

def classify_text_chunks(text_chunks, classifier):
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
    
    # calculate percentage of toxic comments
    n_toxic = classifications.count("toxic")
    n_comments = len(classifications)
    pct_toxic = n_toxic / n_comments

    # identify if there are any toxic comment
    if "toxic" in classifications:
        toxic = True
    else:
        toxic = False


    return classifications, pct_toxic, toxic

# apply function to all text chunks in dataframe
for index, row in data.iterrows():
    # get text chunks
    text_chunks = row["text_chunks"][0]

    # classify text chunks
    classifications, pct_toxic, toxic = classify_text_chunks(text_chunks, classifier)

    # save pct toxic and toxic to dataframe
    data.at[index, "pct_toxic"] = pct_toxic
    data.at[index, "any_toxic"] = toxic

# write to csv
data.to_csv("data/top-youtubers-with-text-and-classifications.csv", index = False)

