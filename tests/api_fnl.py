#app.py
from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename
from flask_cors import CORS
 
app = Flask(__name__)
 
app.secret_key = "svas2023"
 
UPLOAD_FOLDER = 'G:/My Drive/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
def test1():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message' : 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

def test2():
    return 'Test 2'

def test3():
    return 'Test 3'

def test4():
    return 'Test 4'

def test5():
    return 'Test 5'

switch = {
    '1': test1,
    '2': test2,
    '3': test3,
    '4': test4,
    '5': test5,
}

@app.route('/<string:case>',methods=['POST'])
def tests(case):
    received_data = request.data  # Get the raw data received in the request
    print("Received data:", received_data)

    if case in switch:
        return switch[case]()
    else:
        return jsonify({'error':'Invalid test selected'})

 
# Original code: 
# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # check if the post request has the file part
#     if 'files[]' not in request.files:
#         resp = jsonify({'message' : 'No file part in the request'})
#         resp.status_code = 400
#         return resp
 
#     files = request.files.getlist('files[]')
     
#     errors = {}
#     success = False
     
#     for file in files:      
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             success = True
#         else:
#             errors[file.filename] = 'File type is not allowed'
 
#     if success and errors:
#         errors['message'] = 'File(s) successfully uploaded'
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp
#     if success:
#         resp = jsonify({'message' : 'Files successfully uploaded'})
#         resp.status_code = 201
#         return resp
#     else:
#         resp = jsonify(errors)
#         resp.status_code = 500
#         return resp
 
CORS(app,resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
