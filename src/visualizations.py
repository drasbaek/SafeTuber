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



def main():
    # define paths
    results_path = define_paths()

    # load data
    data = pd.read_csv(results_path / "top-youtubers-classified.csv")

    print(data.head())

    # plot share of toxic channels
    plot_share_of_toxic(data, results_path)


if __name__ == "__main__":
    main()
