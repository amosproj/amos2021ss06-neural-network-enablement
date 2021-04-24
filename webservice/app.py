from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
#from flask_uploads import UploadSet,configure_uploads,IMAGES,DATA,ALL
import os
from werkzeug.utils import secure_filename
from helpers import allowed_file

# set path to store uploaded pics and videos
UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + "/static/"
# limit type of extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif','mp4'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'asd_5#y2L"z\n\xec]/'

@app.route('/')
def index():
    return redirect("/upload")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # POST,
    # get the pics and videos
    # check if file
    if request.method == 'POST':
        # get uploaded pics/videos list
        files = request.files.getlist("file")
        files_l = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                files_l.append(filename)
                # save file
                # folderpath = os.path.join(app.config['UPLOAD_FOLDER'], datetime.now().strftime('%Y%m%d%H%M%S'))
                # if not os.path.exists(folderpath):
                #     os.makedirs(folderpath, 755)
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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)

if __name__ == '__main__':
    app.run()
