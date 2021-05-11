from flask import Flask, jsonify, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import datetime
import shutil
from pipeline import colorize_image

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"
# limit type of extensions
ALLOWED_EXTENSIONS = {'pic' : ['png', 'jpg', 'jpeg', 'gif'],'video' : ['mp4', 'mkv', 'webm']}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'wu8QvPtCDIM1/9ceoUS'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload/', methods=['POST'])
def upload():
    # get the pics and videos
    file = request.files.get("file")
    if file and allowed_file(file.filename):
        sfilename = secure_filename(file.filename)
        # add timestamp at the beginning of filename
        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = str(nowTime) + "_" + sfilename
        # create folder and save file
        folderpath = os.path.join(UPLOAD_FOLDER,filename.rsplit('.', 1)[0])
        os.mkdir(folderpath)
        filepath = os.path.join(folderpath,filename)
        file.save(filepath)
        return jsonify(msg="Upload successfully"), 200
    elif file and not allowed_file(file.filename):
        return jsonify(msg ="The file format is not supported"), 400
    else:
        return jsonify(msg ="No upload file"), 400


# create url to sent files
@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    folderpath = os.path.join(UPLOAD_FOLDER,filename.rsplit('.', 1)[0])
    return send_from_directory(folderpath,
                               filename)


#return list of all urls of uploaded files
@app.route('/all/')
def all():
    urls =[]
    for root,dirs,files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if file.rsplit('.', 1)[1].lower() in (ALLOWED_EXTENSIONS['pic'] or ALLOWED_EXTENSIONS['video']):
                urls.append(url_for("uploaded_file", filename=file))
    return jsonify(urls)


# #delete files
@app.route('/delete/', methods=['POST'])
def delete():
    filename = request.get_json()['name'] if 'name' in request.get_json() else None

    if filename:
        deletepath = os.path.join(app.config['UPLOAD_FOLDER'],filename.rsplit('.', 1)[0])
        if os.path.exists(deletepath):
            shutil.rmtree(deletepath)
            return jsonify(msg = "Deleted!"), 200
        else:
            return jsonify(msg = "Pictures not found!"), 404
    else:
        return jsonify(msg = "request is empty"), 400


#colorize files
@app.route('/colorize/',methods=['POST'])
def colorize():

    filename = request.get_json()['name'] if 'name' in request.get_json() else None
    if filename:
        fpath = os.path.join(UPLOAD_FOLDER, filename.rsplit('.', 1)[0])
        # colorize_image
        if filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS['pic']:
            # colorize_image() return value need further discussion
            if colorize_image(fpath, fpath) == True:
                # return page need further discussion
                return render_template("result.html")
            else:
                return jsonify("Colorization failed"),400

        else:
            return jsonify("The format is not supported"),400
    else:
        return jsonify("No input file"), 400




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in (ALLOWED_EXTENSIONS['pic'] or ALLOWED_EXTENSIONS['video'])


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "development"
    app.run()
