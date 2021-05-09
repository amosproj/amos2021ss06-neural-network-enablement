from flask import Flask, jsonify,render_template, request, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import datetime
import shutil
#from pipeline import colorize_image

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


@app.route('/upload/', methods=['POST'])
def upload():
    # get the pics and videos
    # TODO change store folder of pictures
    # get uploaded pics/videos list
    # 4/29 by Xiangxiang Chen, remove loop for file list
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
            if file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
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


# # colorize files
# @app.route('/colorize',methods=['POST'])
# def colorize():
#     if request.method == 'POST':
#         # 1 get file list
#         # 2 loop
#         # 3 identify type of file, video->colorize_video , img-> colorize_image
#         filename = request.get_json()['name'] if 'name' in request.get_json() else None
#
#         # get the name of file chosen by user
#         filenames = request.get_json()['name'] if 'name' in request.get_json() else None
#         # in discussion,so far, use UPLOAD_FOLDER
#         image_path_input = UPLOAD_FOLDER
#
#
#         # colorize_image() = [data from host to device, preprocess, inference, postprocess,data from device to host]
#         colorize_image(image_path_input,image_path_output)
#
#         return render_template("result.html")

# # if this router is needed then present result on a webpage, if not then just delete
# @app.route('/result')
# def result():
#     #TODO
#     return render_template("result.html")

#return json for all orgin and colorized pics
# @app.route('/showresults')
# def showresults():
#     # TODO, an example
#     # {
#     #     all: [
#     #         {original_image: uploaded / image.png,
#     #          converted_image: url / converted.png,
#     #          thumbnail_image: url / thumbnail.png, (needed for videos)
#     #          },
#     #         {next image...}
#     # ]
#     # }
#     return jsonify(results)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    os.environ['FLASK_ENV'] = "development"
    app.run()
