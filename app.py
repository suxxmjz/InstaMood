from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import pandas as pd
from filter import authenticate_to_instagram, build_scraper, scrape_data, add_sentiment
from plot import plotGraphs
import vars
import io
import zipfile

app = Flask(__name__)

@app.route('/styles/<path:filename>')
def custom_static(filename):
    return send_from_directory('styles', filename)

@app.route('/')
def index():
    return redirect(url_for('authenticate'))

@app.route('/export_images')
def export_images():
    pie_path = request.args.get('pie_path')
    scatter_path = request.args.get('scatter_path')
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        pie_image_data = open("/static/" + pie_path, 'rb').read()
        zip_file.writestr('pie_image.png', pie_image_data)

        scatter_image_data = open("/static/" + scatter_path, 'rb').read()
        zip_file.writestr('scatter_image.png', scatter_image_data)
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, attachment_filename='images.zip')

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
    pie_path, scatter_path = plotGraphs(df, post_id)
    
    return render_template('dashboard.html', pie_image=pie_path, scatter_image=scatter_path)

if __name__ == "__main__":
    app.run(debug=True)
