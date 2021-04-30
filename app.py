from flask import Flask, redirect, url_for, render_template, request
import os
import sys
import requests
from PIL import Image

app = Flask(__name__, template_folder='template')

@app.route("/", methods=['GET', 'POST'])
def home():
    images = os.listdir('static/images/')
    
    errors = []
    widthList = []
    heightList = []
    image_tuples = []
    count = 0

    img_param = {
        "more_width" : 0,
        "less_width" : sys.maxsize,
        "more_height" : 0,
        "less_height" : sys.maxsize}

    # add request validation
    if request.method == "POST":
        print("POST REQUEST - my")
        try:
            if (request.form['more_width'] != ""):
                img_param["more_width"] = int(request.form['more_width'])
            if (request.form['less_width'] != ""):
                img_param["less_width"] = int(request.form['less_width'])
            if (request.form['more_height'] != ""):
                img_param["more_height"] = int(request.form['more_height'])
            if (request.form['less_height'] != ""):
                img_param["less_height"] = int(request.form['less_height'])
            #print(img_param)
        except Exception as e:
            print (e)
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    print(img_param["more_width"])
    print(img_param["less_width"])
    print(img_param["more_height"])
    print(img_param["less_height"])

    for item in images:
        im = Image.open('static/images/' + item)
        width, height = im.size  



        if (img_param["more_width"] <= width 
        and  img_param["less_width"] >= width
        and  img_param["more_height"] <= height
        and  img_param["less_height"] >= height):
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