from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import time

from svasModels import ANX_FA_VO

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploaded'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit maximum upload size to 16MB

def save_blob_as_file(blob_data, filename):
    if blob_data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with open(file_path, 'wb') as file:
            file.write(blob_data)

        return file_path
    else:
        return None
    
def save_text(data,filename):
    if data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'w') as file:
            file.write(data)
        return file_path
    else:
        return None

def remove_files():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)

@app.route('/update/<case>', methods=['POST'])
def upload_files(case):

    switch = {
        1: "ANX_FA_VO",
        2: "DEP_FA_VO_TE",
    }


    audio_blob = request.files.get('audioData') #Can be both val and null
    image_blob = request.files.get('imageData') #Can be both val and null
    #video_blob = request.files.get('videoData') #Can be both val and null
    textData = request.form.get('textData')

    if not audio_blob or not image_blob or (textData == "null"):
        if ((audio_blob == None) and image_blob and (textData != "null")):
            remove_files()
            time.sleep(2)
            image_filename = 'image.png'
            text_filename = 'text.txt'
            image_file_path = save_blob_as_file(image_blob.read(), image_filename)
            text_file_path = save_text(textData, text_filename)
            return jsonify({'message': f'{audio_blob} for audio selected, files saved'})
        elif ((image_blob == None) and audio_blob and (textData != "null")):
            remove_files()
            time.sleep(2)
            audio_filename = 'audio.wav'
            text_filename = 'text.txt'
            audio_file_path = save_blob_as_file(audio_blob.read(), audio_filename)
            text_file_path = save_text(textData, text_filename)
            return jsonify({'message': f'{image_blob} for image selected, files saved'})
        elif ((textData == "null") and audio_blob and image_blob):
            remove_files()
            time.sleep(2)
            audio_filename = 'audio.wav'
            image_filename = 'image.png'
            audio_file_path = save_blob_as_file(audio_blob.read(), audio_filename)
            image_file_path = save_blob_as_file(image_blob.read(), image_filename)
            return jsonify({'message': f'{textData} for text selected, files saved'})
        elif ((audio_blob == None) and (image_blob == None) and (textData != "null")):
            remove_files()
            time.sleep(2)
            text_filename = 'text.txt'
            text_file_path = save_text(textData, text_filename)
            return jsonify({'message': f'{audio_blob} for audio and {image_blob} for image selected, files saved'})
        elif ((audio_blob == None) and image_blob and (textData == "null")):
            remove_files()
            time.sleep(2)
            image_filename = 'image.png'
            image_file_path = save_blob_as_file(image_blob.read(), image_filename)
            return jsonify({'message': f'{audio_blob} for audio and {textData} for text selected, files saved'})
        elif ((audio_blob and (image_blob == None) and (textData == "null"))):
            remove_files()
            time.sleep(2)
            audio_filename = 'audio.wav'
            audio_file_path = save_blob_as_file(audio_blob.read(), audio_filename)
            return jsonify({'message': f'{image_blob} for image and {textData} for text selected, files saved'})

    audio_filename = 'audio.wav'
    image_filename = 'image.png'
    text_filename = 'text.txt'

    remove_files()
    time.sleep(2)

    audio_file_path = save_blob_as_file(audio_blob.read(), audio_filename)
    image_file_path = save_blob_as_file(image_blob.read(), image_filename)
    text_file_path = save_text(textData, text_filename)

    if audio_file_path and image_file_path and text_file_path:
        return jsonify({'message': ANX_FA_VO.get_anxiety_level()}), 200
    else:
        return jsonify({'error': 'Failed to upload files'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
