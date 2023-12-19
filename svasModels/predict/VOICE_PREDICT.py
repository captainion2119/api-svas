import librosa
import numpy as np
from tensorflow import keras


sampling_rate = 22050
max_input_length = 286155
emotions = ['Anxiety', 'Happiness', 'Sadness']
test_audio_clip_path = 'uploaded/audio.wav'

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

def voice_predict(case):
    # Load the voice model
    voice_model = keras.models.load_model('models/voice_model_final.h5')
    # Preprocess the test audio clip
    test_features = load_and_preprocess_audio(test_audio_clip_path)
    predicted_probabilities = voice_model.predict(np.expand_dims(test_features, axis=0))

    emotion_index = case - 1
    print(predicted_probabilities[0][emotion_index] * 100)
    return f"{predicted_probabilities[0][emotion_index] * 100:.2f}"

    # class_labels = emotions
    # predicted_class_label = class_labels[np.argmax(predicted_probabilities)]
    # print(f"Predicted Emotion: {predicted_class_label}")
    # for i, class_label in enumerate(class_labels):
    #     probability = predicted_probabilities[0][i]
    #     print(f"Probability of {class_label}: {probability:.2f}")

# 1 -> anxiety
# 2 -> depression
# 3 -> happiness

# print(voice_predict(1))
# print(voice_predict(2))
# print(voice_predict(3))