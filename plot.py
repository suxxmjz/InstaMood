from matplotlib import pyplot as plt

def plot_sentiment_counts(df, shortcode):
    graph1 = df.groupby(['post_shortcode', 'sentiment']).count().reset_index()
    graph2 = graph1[graph1['post_shortcode'] == shortcode]

    colors=["#FF0066", "gray", "#00FF00"]

    fig, ax = plt.subplots()
    for t, y, c in zip(graph2["sentiment"], graph2["comment_text"], colors):
        ax.plot([t,t], [0,y], color=c, marker="o", markersize=10, markevery=(1,2))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_ylim(0, None)
    plt.title("Instagram Comment Sentiment", fontsize=15)
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=12)

    plt.show()
