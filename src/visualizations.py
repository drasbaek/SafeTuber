# install packages
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def define_paths():
    """
    Defines path to out folder

    Returns:
        results_path (pathlib.PosixPath): Path to out folder
    """

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
        results_path (pathlib.PosixPath): path to out folder
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
    colors = ['#FF6D6A', '#77DD77']
    sns.set_palette(sns.color_palette(colors))

    # create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))

    # plot pie chart
    ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)

    # set title
    ax.set_title("Top 100: Share of Channels with at Least One Toxic Comment", fontsize=18, fontweight='bold')

    # set background color
    ax.set_facecolor('#F4E3CB')
    fig.patch.set_facecolor('#F4E3CB')

    # save plot
    plt.savefig(results_path / "share-of-toxic-channels.png", dpi=300, bbox_inches='tight')



def plot_toxicity_by_category(data, results_path):
    '''
    Plots a bar chart displaying the share of toxic comments by category.
    Plot is saved as a png file in the out folder.

    Args:
        data (pd.DataFrame): dataframe with the results of the classifier
        results_path (pathlib.PosixPath): path to out folder
    '''

    # get share of toxic comments by category
    share_toxic = data.groupby("categories")["pct_toxic"].mean().reset_index()

    # order by share of toxic comments
    share_toxic = share_toxic.sort_values(by="pct_toxic", ascending=False)

    # set the color palette
    colors = sns.color_palette("RdYlGn", n_colors=16)
    sns.set_palette(colors)

    # create bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="categories", y="pct_toxic", data=share_toxic, ax=ax)

    # set title and axis labels
    ax.set_title("Share of Toxic Comments by Channel Category", fontsize=18, fontweight='bold')
    ax.set_xlabel("Category", fontsize=14)
    ax.set_ylabel("Percentage of Toxic Comments", fontsize=14)

    # space out x-axis labels
    plt.xticks(rotation=45, ha="right")

    # set background color
    ax.set_facecolor('#F4E3CB')
    fig.patch.set_facecolor('#F4E3CB')

    # save plot
    plt.savefig(results_path / "toxicity-by-category.png", dpi=300, bbox_inches='tight')


def plot_most_toxic_channels(data, results_path):
    '''
    Plots a barchart showing the 10 most toxic channels in the top 100 as well as the average for all channels.
    Plot is saved as a png file in the out folder.

    Args:
        data (pd.DataFrame): dataframe with the results of the classifier
        results_path (pathlib.PosixPath): path to out folder
    '''

    # get the 10 most toxic channels
    most_toxic = data.sort_values(by="pct_toxic", ascending=False).head(10)

    # get the average toxicity for all channels
    avg_toxic = data["pct_toxic"].mean()

    # add average to dataframe
    most_toxic = most_toxic.append({"name": "Average (All Channels)", "pct_toxic": avg_toxic}, ignore_index=True)

    # set color palette
    n = len(most_toxic)
    colors = sns.color_palette("Reds_r", n_colors=n)
    sns.set_palette(colors)

    # create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # plot bar chart
    sns.barplot(x="name", y="pct_toxic", data=most_toxic, ax=ax)

    # set title
    ax.set_title("The Most Toxic Channels in the Top 100", fontsize=18, fontweight='bold')

    # set x and y axis labels
    ax.set_xlabel("Channel Name", fontsize=14)
    ax.set_ylabel("Percentage of Toxic Comments", fontsize=14)

    # space out x-axis labels
    plt.xticks(rotation=45, ha="right")

    # set background color
    ax.set_facecolor('#F4E3CB')
    fig.patch.set_facecolor('#F4E3CB')

    # save plot
    plt.savefig(results_path / "most-toxic-channels.png", dpi=300, bbox_inches='tight')



def main():
    # define paths
    results_path = define_paths()

    # load data
    data = pd.read_csv(results_path / "top-youtubers-classified.csv")

    # set style
    sns.set_style("whitegrid")

    # plot share of toxic channels
    plot_share_of_toxic(data, results_path)

    # plot toxicity by category
    plot_toxicity_by_category(data, results_path)

    # plot most toxic channels
    plot_most_toxic_channels(data, results_path)


if __name__ == "__main__":
    main()
