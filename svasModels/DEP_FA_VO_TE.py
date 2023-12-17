import librosa
import numpy as np
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

sampling_rate = 22050
max_input_length = 286155
emotions = ['Anxiety', 'Happiness', 'Sadness']
# Define the path to your saved Random Forest model
model_filename = 'models/text_model.pkl'
test_audio_clip_path = 'uploaded/audio.wav'
example_image_path = 'uploaded/image.png'

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

def get_depression_level():

    # Load the model
    text_model = joblib.load(model_filename)
    # Load the face model
    face_model = keras.models.load_model('models/face_model_final.h5')
    # Load the voice model
    voice_model = keras.models.load_model('models/voice_model_final.h5')


    # Preprocess the test audio clip
    test_features = load_and_preprocess_audio(test_audio_clip_path)

    predicted_probabilities = voice_model.predict(np.expand_dims(test_features, axis=0))

    class_labels = emotions
    predicted_class_label = class_labels[np.argmax(predicted_probabilities)]

    # print(f"Predicted Emotion: {predicted_class_label}")

    for i, class_label in enumerate(class_labels):
        probability = predicted_probabilities[0][i]
        print(f"Probability of {class_label}: {probability:.2f}")

    # Make predictions on an example image
    
    input_shape = (224, 224, 3)
    img = keras.preprocessing.image.load_img(example_image_path, target_size=input_shape[:2])
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0  # Preprocess the image

    predictions = face_model.predict(img)

    for i, emotion in enumerate(emotions):
        print(f'Predicted {emotion}: {predictions[0][i] * 100:.2f}%')

    # Load the TF-IDF vectorizer
    tfidf_vectorizer_filename = 'models/vectorizer.pkl'
    vectorizer = joblib.load(tfidf_vectorizer_filename)

    # Load the text classification model (trained on the filtered dataset)
    text_model_filename = 'models/text_model.pkl'
    text_model = joblib.load(text_model_filename)

    # Define the list of emotion labels based on your filtered dataset
    emotion_labels = ["happy", "sadness", "anger"]

    # Get user input
    # user_input = input("Enter text: ")

    with open('uploaded/text.txt', 'r') as file:
        content = file.read()

    # Transform user input using the loaded vectorizer
    user_input_tfidf = vectorizer.transform([content])

    # Make a prediction on user input
    predicted_emotion_label = text_model.predict(user_input_tfidf)[0]

    # Get the predicted probabilities for the emotion classes
    predicted_prob = text_model.predict_proba(user_input_tfidf)

    # Print the predicted emotion and probabilities
    # print("\nPredicted emotion:", predicted_emotion_label)
    # print("\nPredicted probabilities:")
    # for label, probability in zip(emotion_labels, predicted_prob[0]):
    #     print(f"{label}: {probability:.2f}")

    voice_probabilities = predicted_probabilities[0]

    face_probabilities = predictions[0]

    text_probabilities = predicted_prob[0]

    voice_classes = ['Sadness', 'Happiness', 'Anxiety']
    face_classes = ['Sadness', 'Happiness', 'Anxiety']
    text_classes = ['happy', 'sadness', 'anger']

    average_happy = (voice_probabilities[1] + face_probabilities[1] + text_probabilities[0]) / 3.0
    average_sad = (voice_probabilities[0] + face_probabilities[0] + text_probabilities[1]) / 3.0


    average_anxiety = (voice_probabilities[2] + face_probabilities[2]) / 2.0


    emotion_labels = ["Happy", "Sad", "Anxiety"]

    # Normalization
    total_probability = average_happy + average_sad + average_anxiety
    normalized_sad = average_sad / total_probability
    # normalized_happy = average_happy / total_probability
    # normalized_anxiety = average_anxiety / total_probability

    # print("Integrated Probabilities of Depression:")
    # print(f"Happy: {normalized_happy:.2f}%")
    # print(f"Sad: {normalized_sad:.2f}%")
    # print(f"Anxiety: {normalized_anxiety:.2f}%")    

    return normalized_sad

get_depression_level()