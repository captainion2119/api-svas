import librosa
import numpy as np
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

# Load the face model
face_model = keras.models.load_model('models/face_model_final.h5')

# Load the voice model
voice_model = keras.models.load_model('models/voice_model_final.h5')

sampling_rate = 22050
max_input_length = 286155
emotions = ['Anxiety', 'Happiness', 'Sadness']

# Load and preprocess the image
def load_and_preprocess_audio(file_path, target_length=max_input_length):
    audio, _ = librosa.load(file_path, sr=sampling_rate, duration=None)

    # Pad or truncate audio to the target length
    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), 'constant')
    else:
        audio = audio[:target_length]

    # Extract features (as before)
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sampling_rate, n_mfcc=13), axis=1)
    chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sampling_rate), axis=1)
    mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sampling_rate), axis=1)

    return np.concatenate((mfccs, chroma, mel))

test_audio_clip_path = 'uploaded/audio.wav'

# Preprocess the test audio clip
test_features = load_and_preprocess_audio(test_audio_clip_path)