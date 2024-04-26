from filter import authenticate_to_instagram, build_scraper, scrape_data, add_sentiment
from plot import plotGraphs
import pandas as pd
import vars

def main():
    authenticate_to_instagram(vars.fireFoxPath)
    build_scraper(vars.username)
    scrape_data(vars.shortcode)
    
    add_sentiment(vars.shortcode)
    
    
    df = pd.read_csv('post_data/' + vars.shortcode + '.csv')
    plotGraphs(df, vars.shortcode)

if __name__ == "__main__":
    main()
