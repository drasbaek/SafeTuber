import pandas as pd
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
def define_paths():
    # define path
    path = Path(__file__)

    # data path
    results_path = path.parents[1] / "out"

    return results_path

def plot_share_of_toxic(data, results_path):
    '''
    Plots a piechart displaying the share of youtube channels with at least one toxic comment.
    Plot is saved as a png file in the out folder.

    Args:
        data (pd.DataFrame): dataframe with the results of the classifier
    '''
    # get share of toxic channels
    toxic_channels = data[data["n_toxic"] > 0]

    # get share of toxic channels
    n_toxic_channels = len(toxic_channels)

    # get share of non-toxic channels
    n_non_toxic_channels = len(data) - n_toxic_channels

    # create labels
    labels = ["Has Toxic Comments", "Does not have Toxic Comments"]

    # create values
    values = [n_toxic_channels, n_non_toxic_channels]

    # set the color palette
    colors = ['#FF6E78', '#50C878']
    sns.set_palette(sns.color_palette(colors))

    # create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))

    # plot pie chart
    ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)

    # set title
    ax.set_title("Top 100: Share of channels with at least one toxic comment")

    # save plot
    plt.savefig(results_path / "share-of-toxic-channels.png")

def plot_toxicity_by_category(data, results_path):
    '''
    Plots a bar chart displaying the share of toxic comments by category.
    Plot is saved as a png file in the out folder.

    Args:
        data (pd.DataFrame): dataframe with the results of the classifier
    '''
    # get share of toxic comments by category
    share_toxic = data.groupby("categories")["pct_toxic"].mean().reset_index()

    # order by share of toxic comments
    share_toxic = share_toxic.sort_values(by="pct_toxic", ascending=False)

    # set the color palette
    #colors = ['#FF6E78', '#50C878']
    #sns.set_palette(sns.color_palette(colors))

    # create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # plot bar chart
    sns.barplot(x="categories", y="pct_toxic", data=share_toxic, ax=ax)

    # set title
    ax.set_title("Share of toxic comments by channel category")

    # space out x-axis labels
    plt.xticks(rotation=45, ha="right")

    # save plot
    plt.savefig(results_path / "toxicity-by-category.png")

def plot_most_toxic_channels(data, results_path):
    '''
    Plots a barchart showing the 10 most toxic channels in the top 100 as well as the average for all channels.
    Plot is saved as a png file in the out folder.
    '''
    # get the 10 most toxic channels
    most_toxic = data.sort_values(by="pct_toxic", ascending=False).head(10)

    # get the average toxicity for all channels
    avg_toxic = data["pct_toxic"].mean()

    # add average to dataframe
    most_toxic = most_toxic.append({"name": "Top 100 Average", "pct_toxic": avg_toxic}, ignore_index=True)

    # create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # plot bar chart
    sns.barplot(x="name", y="pct_toxic", data=most_toxic, ax=ax)

    # set title
    ax.set_title("The most toxic channels in the top 100")

    # space out x-axis labels
    plt.xticks(rotation=45, ha="right")

    # save plot
    plt.savefig(results_path / "most-toxic-channels.png")


def main():
    # define paths
    results_path = define_paths()

    # load data
    data = pd.read_csv(results_path / "top-youtubers-classified.csv")

    # plot share of toxic channels
    plot_share_of_toxic(data, results_path)

    # plot toxicity by category
    plot_toxicity_by_category(data, results_path)

    # plot most toxic channels
    plot_most_toxic_channels(data, results_path)


if __name__ == "__main__":
    main()
