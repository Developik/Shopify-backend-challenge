from flask import Flask, redirect, url_for, render_template
import os
from PIL import Image

app = Flask(__name__, template_folder='template')

@app.route("/")
def home():
    images = os.listdir('static/images/')
    
    widthList = []
    heightList = []

    for item in images:
        im = Image.open('static/images/' + item)
        width, height = im.size  
        widthList.append(width)
        heightList.append(height)

    return render_template("index.html", images = images, widthList = widthList, heightList = heightList)

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