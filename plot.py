from matplotlib import pyplot as plt
import pandas as pd
import os

def plotGraphs(df, shortcode):
    scatter_path = f'static/{shortcode}_scatter.png'
    bar_path = f'static/{shortcode}_bar.png'

    scatter_name =  f'{shortcode}_scatter.png'
    bar_name = f'{shortcode}_bar.png'
    
    plotScatter(df, shortcode, scatter_path)
    plotBar(df, shortcode, bar_path)
    
    return scatter_name, bar_name

def plotScatter(df, shortcode, fig_path):
    plt.figure(figsize=(10, 6))
    polarity_counts = df.groupby('sentiment').size()
    polarity_counts.plot(kind='bar', alpha=0.6)
    plt.title(f"Number of Comments vs. Sentiment for Post {shortcode}", fontsize=15)
    plt.xlabel("Sentiment Polarity", fontsize=12)
    plt.ylabel("Number of Comments", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()

def plotBar(df, shortcode, fig_path):
    plt.figure(figsize=(10, 6))
    plt.scatter(df['comment_timestamp'], df['text_polarity'], alpha=0.6)
    plt.title(f"Sentiment Polarity Over Time for Post {shortcode}", fontsize=15)
    plt.xlabel("Comment Timestamp", fontsize=12)
    plt.ylabel("Sentiment Polarity", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
