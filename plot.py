from matplotlib import pyplot as plt
import pandas as pd
import os

def plotGraphs(df, shortcode):
    pie_path = f'static/{shortcode}_pie.png'
    scatter_path = f'static/{shortcode}_scatter.png'

    pie_name =  f'{shortcode}_pie.png'
    scatter_name = f'{shortcode}_scatter.png'

    if not os.path.exists('static'):
        os.makedirs('static')
    
    plotPie(df, shortcode, pie_path)
    plotBar(df, shortcode, scatter_path)
    
    return pie_name, scatter_name

def plotPie(df, shortcode, fig_path):
    polarity_counts = df.groupby('sentiment').size()

    colors = ['#ff9999', '#66b3ff', '#99ff99']

    plt.figure(figsize=(8, 8))
    plt.pie(polarity_counts, labels=polarity_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title(f"Number of Comments vs. Sentiment for Post {shortcode}", fontsize=15)
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
