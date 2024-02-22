from glob import glob
from os.path import expanduser
from sqlite3 import connect
import pathlib
import csv
import emoji
import pandas as pd
from matplotlib import pyplot as plt
from instaloader import Instaloader, ConnectionException, Post
from textblob import TextBlob

def authenticate_to_instagram():
    path_to_firefox_cookies = XXXPATH
    FIREFOXCOOKIEFILE = glob(expanduser(path_to_firefox_cookies))[0]

    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(connect(FIREFOXCOOKIEFILE)
                                                .execute("SELECT name, value FROM moz_cookies "
                                                        "WHERE host='.instagram.com'"))
    
    try:
        username = instaloader.test_login()
        if not username:
            raise ConnectionException()
    except ConnectionException:
        raise SystemExit("Cookie import failed. Are you logged in successfully in Firefox?")
    
    instaloader.context.username = username
    instaloader.save_session_to_file()

def build_scraper():
    global instagram
    instagram = Instaloader(download_pictures=False, download_videos=False,
                                    download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)
    instagram.load_session_from_file(XXXUSERNAME)

def scrape_data(url):
    SHORTCODE = str(url[28:39])
    post = Post.from_shortcode(instagram.context, SHORTCODE)

    csvName = SHORTCODE + '.csv'
    output_path = pathlib.Path('post_data')
    output_path.mkdir(parents=True, exist_ok=True)
    post_file = output_path.joinpath(csvName).open("w", encoding="utf-8")

    field_names = [
                "post_shortcode",
                "commenter_username",
                "comment_text",
                "comment_likes"
                ]

    post_writer = csv.DictWriter(post_file, fieldnames=field_names)
    post_writer.writeheader()

    for x in post.get_comments():
        post_info = {
        "post_shortcode":post.shortcode,
        "commenter_username": x.owner,
        "comment_text": (emoji.demojize(x.text)).encode('utf-8', errors='ignore').decode() if x.text else "",
        "comment_likes": x.likes_count
        }

        post_writer.writerow(post_info)

    print("Done Scraping!")

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def add_sentiment():
    df = pd.read_csv('post_data/XXXCODE.csv')
    df['text_polarity'] = df['comment_text'].apply(getPolarity)
    df['sentiment'] = pd.cut(df['text_polarity'], [-1, -0.0000000001, 0.0000000001, 1], labels=["Negative", "Neutral", "Positive"])
    df.to_csv('post_data/XXXCODE.csv', index=False)

def plot_sentiment_counts(df, shortcode):
    graph1 = df.groupby(['post_shortcode', 'sentiment']).count().reset_index()
    graph2 = graph1[graph1['post_shortcode'] == shortcode]

    colors = colors=["#FF0066", "gray", "#00FF00"]

    fig, ax = plt.subplots()
    for t, y, c in zip(graph2["sentiment"], graph2["comment_text"], colors):
        ax.plot([t,t], [0,y], color=c, marker="o", markersize=10, markevery=(1,2))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_ylim(0, None)
    plt.title("Instagram Comment Sentiment", fontsize=15)
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=12)

    plt.show()

def main():
    authenticate_to_instagram()
    build_scraper()
    
    url = "https://www.instagram.com/p/XXXCODE/"
    scrape_data(url)
    
    add_sentiment()
    
    df = pd.read_csv('post_data/XXXCODE.csv')
    shortcode = 'XXXCODE'
    plot_sentiment_counts(df, shortcode)

if __name__ == "__main__":
    main()
