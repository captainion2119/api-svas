from flask import Flask, json, request, jsonify
import os
import urllib.request
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit maximum upload size to 16MB

@app.route('/1', methods=['POST'])
def upload_files():
    if 'audioData' not in request.files or 'imageData' not in request.files:
        return jsonify({'error': 'Missing audioData or imageData'}), 400

    audio_file = request.files['audioData']
    image_file = request.files['imageData']

    print(audio_file)
    print(image_file)

    if audio_file.filename == '' or image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if audio_file and image_file:
        audio_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio_file.filename))
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))

        audio_file.save(audio_filename)
        image_file.save(image_filename)

        return jsonify({'message': 'Files uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Failed to upload files'}), 500

if __name__ == '__main__':
    app.run(debug=True)
