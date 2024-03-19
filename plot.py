from matplotlib import pyplot as plt
import pandas as pd


def plotGraphs(df, shortcode):
    plotScatter(df, shortcode)
    plotBar(df, shortcode)
    plt.show()



def plotScatter(df, shortcode):
    df['comment_timestamp'] = pd.to_datetime(df['comment_timestamp'])

    plt.figure(figsize=(10, 6))
    
    polarity_counts = df.groupby('sentiment').size()

    polarity_counts.plot(kind='bar', alpha=0.6)

    plt.title(f"Number of Comments vs. Sentiment for Post {shortcode}", fontsize=15)
    plt.xlabel("Sentiment Polarity", fontsize=12)
    plt.ylabel("Number of Comments", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    

def plotBar(df, shortcode):
    df['comment_timestamp'] = pd.to_datetime(df['comment_timestamp'])

    plt.figure(figsize=(10, 6))
    plt.scatter(df['comment_timestamp'], df['text_polarity'], alpha=0.6)
    
    plt.title(f"Sentiment Polarity Over Time for Post {shortcode}", fontsize=15)
    plt.xlabel("Comment Timestamp", fontsize=12)
    plt.ylabel("Sentiment Polarity", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
