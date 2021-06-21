from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import datetime
import shutil
import colorization.pipeline as pipeline

# from colorization.src.pipeline import *

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"
# limit type of extensions
ALLOWED_EXTENSIONS = {
    'pic': ['png', 'jpg', 'jpeg', 'gif'],
    'video': ['mp4', 'mkv', 'webm']
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'wu8QvPtCDIM1/9ceoUS'


@app.get('/')
def index():
    '''
    This endpoint displays the main html file.
    Further functionality is provided via javascript.

    Return type: html
    '''
    return render_template("index.html")


@app.post('/upload/')
def upload():
    '''
    This endpoint accepts a single image/video
    and stores it in the folder specified in
    app.config['UPLOAD_FOLDER']

    Return type: json
    '''
    file = request.files.get("file")
    if file and allowed_file(file.filename):
        sfilename = secure_filename(file.filename)

        # add timestamp at the beginning of filename
        nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = str(nowtime) + "_" + sfilename

        # create folder and save file
        folderpath = os.path.join(app.config['UPLOAD_FOLDER'], get_name(filename))
        os.mkdir(folderpath)
        filepath = os.path.join(folderpath, filename)
        file.save(filepath)

        return jsonify(msg="Upload successfully"), 200

    elif file and not allowed_file(file.filename):
        return jsonify(msg="The file format is not supported"), 400

    else:
        return jsonify(msg="No upload file"), 400


@app.get('/<fpath>/<filename>')
def uploaded_file(fpath, filename):
    '''
    This endpoint returns the image located at the given path

    Return type: image
    '''
    folderpath = os.path.join(UPLOAD_FOLDER, fpath)
    return send_from_directory(folderpath, filename)


@app.get('/all/')
def all():
    '''
    This endpoint returns a list of the urls of all uploaded images/videos

    Return type: json
    '''
    urls = []
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for filename in files:
            if allowed_file(filename):
                name = get_name(filename)
                # exclude the colored file
                if name.rsplit("_", 1)[1] != "color":
                    urls.append(url_for("uploaded_file", fpath=name, filename=filename))
    return jsonify(urls)


# TODO: This should be a GET request
@app.post('/result/')
def result():
    '''
    This endpoint returns the urls of the given image/video (specified by its filename)
    the colorized version of it.

    Return type: json
    '''
    filename = request.get_json()['name'] if 'name' in request.get_json() else None

    # get name and extension of origin img
    name = get_name(filename)
    extension = get_extension(filename)
    # get name of colored img
    colorname = name + "_color." + extension

    # if is a video, get thumbnail img name
    thumbnailname = name + "_thumbnail." + extension

    # generate all urls
    origin_url = url_for("uploaded_file", fpath=name, filename=filename)
    colorized_url = url_for("uploaded_file", fpath=name, filename=colorname)
    thumbnail_url = url_for("uploaded_file", fpath=name, filename=thumbnailname)

    result = {
        'origin': origin_url,
        'colorized': colorized_url,
        'thumbnail': thumbnail_url
    }

    return jsonify(result), 200


@app.post('/delete/')
def delete():
    '''
    This endpoint deletes the image/video (specified by its filename)

    Return type: json
    '''
    filename = request.get_json()['name'] if 'name' in request.get_json() else None

    if filename:
        deletepath = os.path.join(app.config['UPLOAD_FOLDER'], get_name(filename))
        if os.path.exists(deletepath):
            shutil.rmtree(deletepath)
            return jsonify(msg="Deleted!"), 200
        else:
            return jsonify(msg="Pictures not found!"), 404
    else:
        return jsonify(msg="request is empty"), 400


# colorize files
@app.post('/colorize/')
def colorize():
    '''
    This endpoint starts the colorizing process for the given image/video
    (specified by its filename)

    Return type: json
    '''
    filename = request.get_json()['name'] if 'name' in request.get_json() else None

    if filename:
        # 05/20 use newly added functions : get_name , get_extension
        name = get_name(filename)
        extension = get_extension(filename)

        finpath = os.path.join(app.config['UPLOAD_FOLDER'], name, filename)
        optfilename = name + "_color." + extension
        foutpath = os.path.join(app.config['UPLOAD_FOLDER'], name, optfilename)

            # colorize_image
        if extension.lower() in ALLOWED_EXTENSIONS['pic']:
            # temporarily use if True
            if pipeline.colorize_image(finpath, foutpath) == 0:
                # return page need further discussion
                return jsonify(msg="Colorization successful."), 200
            else:
                return jsonify(msg="Colorization failed."), 400
        else:
            return jsonify(msg="Videos are not supported yet."), 400

    else:
        return jsonify(msg="No input file"), 400


def allowed_file(filename):
    return '.' in filename and get_extension(filename).lower() in (
            ALLOWED_EXTENSIONS['pic'] or ALLOWED_EXTENSIONS['video'])


def get_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_name(filename):
    return filename.rsplit('.', 1)[0]


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "development"
    app.run(host='0.0.0.0')
