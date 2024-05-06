from flask import Flask, render_template
import pandas as pd
from filter import authenticate_to_instagram, build_scraper, scrape_data, add_sentiment
from plot import plotGraphs
import vars

app = Flask(__name__)

@app.route('/')
def authenticate_and_plot():
    authenticate_to_instagram(vars.fireFoxPath)
    build_scraper(vars.username)
    scrape_data(vars.shortcode)
    add_sentiment(vars.shortcode)
    
    df = pd.read_csv(f'post_data/{vars.shortcode}.csv')
    scatter_path, bar_path = plotGraphs(df, vars.shortcode)
    
    return render_template('dashboard.html', scatter_image=scatter_path, bar_image=bar_path)

if __name__ == "__main__":
    app.run(debug=True)
