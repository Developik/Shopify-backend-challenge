from flask import Flask, redirect, url_for, render_template
import os
from PIL import Image

app = Flask(__name__, template_folder='template')

@app.route("/")
def home():
    images = os.listdir('static/images/')
    
    widthList = []
    heightList = []
    image_tuples = []
    count = 0

    for item in images:
        im = Image.open('static/images/' + item)
        width, height = im.size  
        widthList.append(width)
        heightList.append(height)
        image_tuples.append([item, count])
        count += 1

    return render_template("index.html", image_tuples = image_tuples, widthList = widthList, heightList = heightList)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)