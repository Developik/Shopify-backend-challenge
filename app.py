from flask import Flask, redirect, url_for, render_template, request
import os
import sys
import requests
from PIL import Image
from requests_toolbelt.multipart import decoder

app = Flask(__name__, template_folder='template')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def home():
    images = os.listdir('static/images/')
    
    errors = []
    widthList = []
    heightList = []
    image_tuples = []
    formatList = []
    filenames = []
    count = 0

    img_param = {
        "more_width" : 0,
        "less_width" : sys.maxsize,
        "more_height" : 0,
        "less_height" : sys.maxsize,
        "img_format" : "All"}

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
            if (request.form['less_height'] != "All"):
                img_param["img_format"] = int(request.form['img_format'])
                if (img_param["img_format"] == 1):
                    img_param["img_format"] = "PNG"
                elif (img_param["img_format"] == 2):
                    img_param["img_format"] = "JPEG"
            #print(img_param):
        except Exception as e:
            print (e)
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    print(img_param["more_width"])
    print(img_param["less_width"])
    print(img_param["more_height"])
    print(img_param["less_height"])
    print(img_param["img_format"])

    for item in images:
        im = Image.open('static/images/' + item)
        width, height = im.size  

        if (img_param["more_width"] <= width 
        and  img_param["less_width"] >= width
        and  img_param["more_height"] <= height
        and  img_param["less_height"] >= height
        and  (img_param["img_format"] == "All" or img_param["img_format"] == im.format)):
            widthList.append(width)
            heightList.append(height)
            image_tuples.append([item, count])
            formatList.append(im.format)
            filenames.append(im.filename)
            count += 1



    return render_template("index.html", image_tuples = image_tuples, widthList = widthList,
     heightList = heightList, formatList = formatList, filenames = filenames)


@app.route("/delete-image", methods=['POST'])
def delete_image():

    images = os.listdir('static/images/')

    #print(request.form['img_id'])
    try:
        os.remove(request.form['img_id']) 
    except Exception:
        pass
    return redirect("/", code=302)

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

@app.route("/image-upload", methods=['POST'])
def upload_image():

    images = os.listdir('static/images/')
    uploaded_image = request.files['myFile']
    if (allowed_file(uploaded_image.filename)):
        uploaded_image.save('./static/images/img'+str(len(images)+1)+'.'+uploaded_image.filename.rsplit('.', 1)[1].lower())

    return redirect("/", code=302)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)