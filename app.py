from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from filter import authenticate_to_instagram, build_scraper, scrape_data, add_sentiment
from plot import plotGraphs

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('authenticate'))

@app.route('/authenticate')
def authenticate():
    authenticate_to_instagram(vars.fireFoxPath)
    build_scraper(vars.username)
    return render_template('authentication.html')

@app.route('/enter_post_id', methods=['GET', 'POST'])
def enter_post_id():
    if request.method == 'POST':
        post_id = request.form['post_id']
        
        return redirect(url_for('dashboard', post_id=post_id))
    
    return render_template('enterPost.html')

@app.route('/dashboard')
def dashboard():
    post_id = request.args.get('post_id')
    if post_id is None:
        return "Error: No post ID provided."
    
    scrape_data(post_id)
    add_sentiment(post_id)
    df = pd.read_csv(f'post_data/{post_id}.csv')
    scatter_path, bar_path = plotGraphs(df, post_id)
    
    return render_template('dashboard.html', scatter_image=scatter_path, bar_image=bar_path)

if __name__ == "__main__":
    app.run(debug=True)
