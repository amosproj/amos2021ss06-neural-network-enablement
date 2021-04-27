from flask import Flask, flash, redirect, jsonify,render_template, request, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/uploaded/"
# limit type of extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','gif','mp4'}

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
        files = request.files.getlist("file")
        files_l = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                files_l.append(filename)
                # save file
                filepath = os.path.join(UPLOAD_FOLDER,filename)
                file.save(filepath)
            elif file and not allowed_file(file.filename):
                flash('The format is not supported. Please change and reload. ')
                return render_template("upload.html")
            else:
                return render_template("upload.html")
        return render_template("uploaded.html", uploaded_file=filepath, files_l=files_l)

    else:
        return render_template("upload.html")

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
        files = request.form.getlist("files")
        if files:
            for file in files:
                fpath = os.path.join(app.config['UPLOAD_FOLDER'], file)
                if os.path.exists(fpath):
                    os.remove(fpath)
        else:
            return jsonify("request is empty")
        return render_template("uploaded.html")
    else:
        return render_template("upload.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run()
