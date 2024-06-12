# Code adapted from Kinnaird, M. (2021). Scraping and Plotting Sentiment of an Instagram Comment Section. Retrieved from https://github.com/madelinekinnaird/instagram-sentiment-tutorial
from glob import glob
from os.path import expanduser
from sqlite3 import connect
import pathlib
import csv
import emoji
import pandas as pd
from instaloader import Instaloader, ConnectionException, Post
from textblob import TextBlob
import vars 

instagram = None

def authenticate_to_instagram(firefox_cookie_path):
    global instagram
    instagram = Instaloader(max_connection_attempts=1)
    
    FIREFOXCOOKIEFILE = glob(expanduser(firefox_cookie_path))[0]
    conn = connect(FIREFOXCOOKIEFILE)
    cookies = conn.execute("SELECT name, value FROM moz_cookies WHERE host='.instagram.com'")
    for name, value in cookies:
        instagram.context._session.cookies.set(name, value)

    try:
        username = instagram.test_login()
        if not username:
            raise ConnectionException("Cookie import failed. Are you logged in successfully in Firefox?")
    except ConnectionException as e:
        raise SystemExit(e)
    
    instagram.context.username = username
    instagram.save_session_to_file()

def build_scraper():
    global instagram
    if instagram is None:
        raise ValueError("Instagram scraper not initialized. Call authenticate_to_instagram first.")

def scrape_data(shortcode):
    global instagram
    if instagram is None:
        raise ValueError("Instagram scraper not initialized. Call build_scraper first.")

    SHORTCODE = shortcode
    post = Post.from_shortcode(instagram.context, SHORTCODE)

    csvName = SHORTCODE + '.csv'
    output_path = pathlib.Path('post_data')
    output_path.mkdir(parents=True, exist_ok=True)
    post_file = output_path.joinpath(csvName).open("w", encoding="utf-8")

    field_names = [
        "post_shortcode",
        "commenter_username",
        "comment_text",
        "comment_likes",
        "comment_timestamp"
    ]

    post_writer = csv.DictWriter(post_file, fieldnames=field_names)
    post_writer.writeheader()

    all_comments = set()

    for x in post.get_comments():
        user_comment = (x.owner, x.text)
        comment_text = emoji.demojize(x.text).encode('utf-8', errors='ignore').decode() if x.text else ""

        if not comment_text:
            continue
        if user_comment not in all_comments:
            all_comments.add(user_comment)
            post_info = {
                "post_shortcode": post.shortcode,
                "commenter_username": x.owner,
                "comment_text": comment_text,
                "comment_likes": x.likes_count,
                "comment_timestamp": x.created_at_utc
            }
            post_writer.writerow(post_info)

    print("Done Scraping!")

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

def add_sentiment(shortcode):
    df = pd.read_csv('post_data/' + shortcode + '.csv')
    df['text_polarity'] = df['comment_text'].apply(get_polarity)
    df['sentiment'] = pd.cut(df['text_polarity'], [-1, -0.0000000001, 0.0000000001, 1], labels=["Negative", "Neutral", "Positive"])
    df.to_csv('post_data/' + shortcode + '.csv', index=False)
