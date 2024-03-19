import datetime
from glob import glob
from os.path import expanduser
from sqlite3 import connect
import pathlib
import csv
import emoji
import pandas as pd
from instaloader import Instaloader, ConnectionException, Post
from textblob import TextBlob


def authenticate_to_instagram(path):
    path_to_firefox_cookies = path
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

def build_scraper(username):
    global instagram
    instagram = Instaloader(download_pictures=False, download_videos=False,
                                    download_video_thumbnails=False, save_metadata=False, max_connection_attempts=0)
    instagram.load_session_from_file(username)

def scrape_data(shortcode):
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

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def add_sentiment(shortcode):
    df = pd.read_csv('post_data/' + shortcode + '.csv')
    df['text_polarity'] = df['comment_text'].apply(getPolarity)
    df['sentiment'] = pd.cut(df['text_polarity'], [-1, -0.0000000001, 0.0000000001, 1], labels=["Negative", "Neutral", "Positive"])
    df.to_csv('post_data/' + shortcode + '.csv', index=False)
