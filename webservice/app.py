from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import datetime
import shutil
import cv2
import colorization.pipeline as pipeline

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"
# limit type of extensions
ALLOWED_EXTENSIONS = {
    'pic': ['png', 'jpg', 'jpeg'],
    'video': ['mp4']
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


@app.post('/media/')
def upload():
    '''
    This endpoint accepts a single image/video
    and stores it in the folder specified in
    app.config['UPLOAD_FOLDER']

    Return type: json
    '''
    file = request.files.get("file")
    if file and valid_filename(file.filename):
        sfilename = secure_filename(file.filename)

        # add timestamp at the beginning of filename
        nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = str(nowtime) + "_" + sfilename

        # create folder and save file
        name = get_name(filename)
        extension = get_extension(filename)

        folderpath = os.path.join(app.config['UPLOAD_FOLDER'], name)
        os.mkdir(folderpath)
        filepath = os.path.join(folderpath, filename)
        file.save(filepath)

        # get and save the thumbnail if the type is video
        if extension in ALLOWED_EXTENSIONS['video']:
            thumbnailname = name + "_thumbnail.jpg"
            thumbnailpath = os.path.join(folderpath, thumbnailname)

            vcap = cv2.VideoCapture(filepath)
            res, thumbnail = vcap.read()
            if res:
                cv2.imwrite(thumbnailpath, thumbnail)
            else:
                return jsonify(msg="Fail to read the video"), 400

        return jsonify(msg="Upload successfully"), 200

    elif file and not valid_filename(file.filename):
        return jsonify(msg="The file format is not supported"), 400

    else:
        return jsonify(msg="No upload file"), 400


@app.get('/media/')
def all():
    '''
    This endpoint returns a list of the urls of all uploaded images/videos

    Return type: json
    '''
    result = []

    folders = filter(lambda x: x != '.keep', os.listdir(app.config['UPLOAD_FOLDER']))

    for folder in folders:
        files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], folder))
        extensions = map(lambda f: get_extension(f).lower(), files)

        if any(map(lambda e: e in ALLOWED_EXTENSIONS['video'], extensions)):
            type = 'video'
        else:
            type = 'image'

        for f in files:
            if type == 'video' and 'thumbnail' in f:
                thumbnail = url_for('uploaded_file', fpath=folder, filename=f)

            elif type == 'image' and get_name(f) == folder:
                thumbnail = url_for("uploaded_file", fpath=folder, filename=f)

        assert 'thumbnail' in locals(), f'thumbnail for {folder} not found'

        result.append({
            'type': type,
            'thumbnail': thumbnail,
            'id': folder
        })

    return jsonify(result)


@app.get('/media/<id>')
def result(id):
    '''
    This endpoint returns the urls of the given image/video (specified by its folder
    name) and of its colorized version.

    Return type: json
    '''
    if id in os.listdir(app.config['UPLOAD_FOLDER']):
        folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
    else:
        return jsonify(msg="The file doesn't exist"), 400

    thumbnail_url = None

    for f in os.listdir(folder):
        if get_name(f) == id:
            # generate urls of the original and colorized files
            origin_url = url_for("uploaded_file", fpath=id, filename=f)

            extension = get_extension(f)

            if extension.lower() in ALLOWED_EXTENSIONS['video']:
                color_name = get_name(f) + "_color.webm"
            else:
                color_name = get_name(f) + "_color." + extension

            colorized_url = url_for("uploaded_file", fpath=id, filename=color_name)

            #  check whether the colorization process is finished
            if os.path.exists(os.path.join(folder, color_name)):
                status = "finished"
            else:
                status = "unfinished"

            # get the type and generate the thumbnail url if it's a video
            if extension.lower() in ALLOWED_EXTENSIONS['pic']:
                type = 'image'
            else:
                type = 'video'
                thumbnail = get_name(f) + "_thumbnail.jpg"
                thumbnail_url = url_for("uploaded_file", fpath=id, filename=thumbnail)

    result = {
        'type': type,
        'status': status,
        'origin': origin_url,
        'colorized': colorized_url,
        'thumbnail': thumbnail_url
    }
    return jsonify(result), 200


@app.delete('/media/<id>')
def delete(id):
    '''
    This endpoint deletes the image/video (specified by its folder name)

    Return type: json
    '''

    if id in os.listdir(app.config['UPLOAD_FOLDER']):
        deletepath = os.path.join(app.config['UPLOAD_FOLDER'], id)
        shutil.rmtree(deletepath)
        return jsonify(msg="Deleted!"), 200
    else:
        return jsonify(msg="Pictures not found!"), 400


# colorize files
@app.post('/media/<id>/colorize')
def colorize(id):
    '''
    This endpoint starts the colorizing process for the given image/video
    (specified by its folder name)

    Return type: json
    '''
    if id in os.listdir(app.config['UPLOAD_FOLDER']):
        folder = os.path.join(app.config['UPLOAD_FOLDER'], id)
    else:
        return jsonify(msg="The file doesn't exist"), 400

    # get the extension(type), input path, output path from the original data
    for f in os.listdir(folder):
        if get_name(f) == id:
            extension = get_extension(f)
            finpath = os.path.join(folder, f)

            if extension.lower() in ALLOWED_EXTENSIONS['video']:
                coloredfile = get_name(f) + "_color.webm"
            else:
                coloredfile = get_name(f) + "_color." + extension

            foutpath = os.path.join(folder, coloredfile)

            if not os.path.exists(foutpath):
                # colorize_image
                if extension.lower() in ALLOWED_EXTENSIONS['pic']:
                    print(f'Starting colorization of {id}')
                    res = pipeline.colorize_image(finpath, foutpath)
                elif extension.lower() in ALLOWED_EXTENSIONS['video']:
                    print(f'Starting colorization of {id}')
                    res = pipeline.colorize_video(finpath, foutpath)
                else:
                    return jsonify(msg="Unsupported file format"), 400

                if res == 0:
                    return jsonify(msg="Colorization successful."), 200
                else:
                    return jsonify(msg="Colorization failed."), 400

            else:
                return jsonify(
                    msg='Colorization file exists. Colorization successful.'), 200


@app.get('/<fpath>/<filename>')
def uploaded_file(fpath, filename):
    '''
    This endpoint returns the image located at the given path

    Return type: image
    '''
    folderpath = os.path.join(UPLOAD_FOLDER, fpath)
    return send_from_directory(folderpath, filename)


def valid_filename(filename):
    '''
    Checks if the given filename is valid.
    '''
    if '.' not in filename:
        return False

    lower_extension = get_extension(filename).lower()
    if lower_extension in ALLOWED_EXTENSIONS['pic'] or lower_extension in \
            ALLOWED_EXTENSIONS['video']:
        return True

    return False


def get_extension(filename):
    return filename.rsplit('.', 1)[1]


def get_name(filename):
    return filename.rsplit('.', 1)[0]


@app.errorhandler(RuntimeError)
def handle_error(e):
    print('------------------')
    print('ERROR HANDLER CALLED')
    print(f'{e.__class__}: {str(e)}')
    print('------------------')
    return jsonify(msg=f'An error occured: {str(e)}'), 500


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "development"
    app.run(host='0.0.0.0')
