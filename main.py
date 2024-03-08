from filter import authenticate_to_instagram, build_scraper, scrape_data, add_sentiment
from plot import plot_sentiment_counts
import pandas as pd

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
