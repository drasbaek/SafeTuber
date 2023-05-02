from transformers import pipeline
import pandas as pd
import tqdm

# load data with transcripts
data = pd.read_csv("data/top-youtubers-curated.csv")

# change text chunks to list
data["text_chunks"] = data["text_chunks"].apply(eval)

# load toxicity classifier
classifier = pipeline("text-classification", model = "unitary/toxic-bert")

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

        print(classification)

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
    pct_toxic = n_toxic / n_comments

    # get a toxic comment
    toxic_comment = text_chunks[classifications.index("toxic")]

    return pct_toxic, toxic_comment

# apply function to all text chunks in dataframe
for index, row in data.iterrows():
    # get text chunks
    text_chunks = row["text_chunks"][0]

    # classify text chunks
    classifications = classify_text_chunks(text_chunks, classifier)

    # calculate toxicity aggregates
    pct_toxic, toxic_comment = toxicity_aggregates(text_chunks, classifications)

    # save to dataframe
    data.at[index, "example_toxic_comment"] = toxic_comment
    data.at[index, "pct_toxic"] = pct_toxic

# write to csv
data.to_csv("data/top-youtubers-with-text-and-classifications.csv", index = False)

