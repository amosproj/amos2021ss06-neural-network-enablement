from flask import Flask, flash, redirect, jsonify,render_template, request, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"
# limit type of extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','mp4', 'mkv', 'webm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'wu8QvPtCDIM1/9ceoUS'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    # POST
    # get the pics and videos
    if request.method == 'POST':
        # get uploaded pics/videos list
        # 4/29 by Xiangxiang Chen, remove loop for file list
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save file
            filepath = os.path.join(UPLOAD_FOLDER,filename)
            file.save(filepath)
            return jsonify(msg="Upload successfully"), 200
        elif file and not allowed_file(file.filename):
            return jsonify(msg ="The file format is not supported"), 400
        else:
            return jsonify(msg ="No upload file"), 400
    else:
        return render_template("index.html")

# create url to sent files
@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)

#return list of all urls of uploaded files
@app.route('/all')
def all():
    names = os.listdir(app.config['UPLOAD_FOLDER'])
    urls = []
    for name in names:
        urls.append(url_for("uploaded_file",filename = name))

    urls.sort()
    urls.reverse()

    return jsonify(urls)

# #delete files
@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        files = request.form.get('files')
        if files:
            deletepath = os.path.join(app.config['UPLOAD_FOLDER'],files)
            if os.path.exists(deletepath):
                os.remove(deletepath)
                return jsonify(msg = "Deleted!"), 200
            else:
                return jsonify(msg = "Pictures not found!"), 404
        else:
            return jsonify(msg = "request is empty"), 400
    else:
        return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "development"
    app.run()
