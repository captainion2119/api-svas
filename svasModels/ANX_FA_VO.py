import librosa
import numpy as np
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator

sampling_rate = 22050
max_input_length = 286155
emotions = ['Anxiety', 'Happiness', 'Sadness']
test_audio_clip_path = 'uploaded/audio.wav'
example_image_path = 'uploaded/image.png'


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

def get_anxiety_level():
    # Load the face model
    face_model = keras.models.load_model('models/face_model_final.h5')
    # Load the voice model
    voice_model = keras.models.load_model('models/voice_model_final.h5')
    # Preprocess the test audio clip
    test_features = load_and_preprocess_audio(test_audio_clip_path)
    predicted_probabilities = voice_model.predict(np.expand_dims(test_features, axis=0))
    # class_labels = emotions
    # predicted_class_label = class_labels[np.argmax(predicted_probabilities)]
    # print(f"Predicted Emotion: {predicted_class_label}")
    # for i, class_label in enumerate(class_labels):
    #     probability = predicted_probabilities[0][i]
    #     print(f"Probability of {class_label}: {probability:.2f}")
    # Make predictions on an example image
    input_shape = (224, 224, 3)
    img = keras.preprocessing.image.load_img(example_image_path, target_size=input_shape[:2])
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0  # Preprocess the image
    predictions = face_model.predict(img)
    # for i, emotion in enumerate(emotions):
        # print(f'Predicted {emotion}: {predictions[0][i] * 100:.2f}%')
    # systolic = 150 # 40% importance
    # diastolic = 150  # 30% importance
    # Pulse = 120  # 30% importance
    # print(f"Systolic: {systolic}mmhg")
    # print(f"Diastolic: {diastolic}mmhg")
    # print(f"Pulse: {Pulse}/min")
    # Physiological parameter values
    # systolic = 150 # 40% importance
    # diastolic = 150  # 30% importance
    # Pulse = 120     # 30% importance
    # # Importance weights
    # weight_sbp = 0.4
    # weight_dbp = 0.3
    # weight_pulse = 0.3
    # # Define normal values for systolic, diastolic, and pulse rate
    # normal_sbp = 120
    # normal_dbp = 80
    # normal_pulse = 75
    # # Calculate the danger importance score with normal values
    # dang_sys = 0
    # dang_dia = 0
    # dang_pul = 0
    # #assigning the danger importance based on lower or higher than the normal limit
    # if (systolic > normal_sbp):
    #     dang_sys = max(abs(systolic - normal_sbp), 0) * weight_sbp
    # elif (systolic < normal_sbp):
    #     dang_sys = abs(min((systolic - normal_sbp),0)) * weight_sbp
    # if (diastolic > normal_dbp):
    #     dang_dia = max(abs(diastolic - normal_dbp), 0)* weight_dbp
    # elif(diastolic < normal_dbp):
    #     dang_dia = abs(min(diastolic - normal_dbp), 0) * weight_dbp
    # if (Pulse > normal_dbp):
    #     dang_pul = max(abs(Pulse - normal_pulse), 0) * weight_pulse
    # elif(Pulse < normal_dbp):
    #     dang_pul = abs(min(Pulse - normal_pulse), 0) * weight_pulse
    # danger_importance = (
    #     dang_sys +
    #     dang_dia +
    #     dang_pul
    # ) / (weight_sbp + weight_dbp + weight_pulse)
    # #print(f"Danger importance: {danger_importance}")
    # #print((danger_importance - min(danger_importance, 1)) / (max(danger_importance, 100) - min(danger_importance, 1))*99)
    # # Normalize the score to a scale of 1 to 100
    # normalized_danger_importance = (danger_importance - min(danger_importance, 1)) / (max(danger_importance, 100) - min(danger_importance, 1)) * 99 + 1
    # Print the danger importance score
    # print(f"Danger Importance: {normalized_danger_importance:.2f}")
    # Weight for danger importance (50%)
    # weight_danger_importance = 0.5
    # normalized_danger = normalized_danger_importance/100
    # Weight for average probabilities (50%)īīīīīīī
    # weight_average_probabilities = 0.5
    average_probabilities = (predicted_probabilities[0] + predictions[0]) / 2
    # print("Integrated Probabilities:")
    # for i, emotion in enumerate(emotions):
    #     integrated_probability = (normalized_danger * weight_danger_importance) + (average_probabilities[i] * weight_average_probabilities)
        #print(normalized_danger_importance * weight_danger_importance)
        #print(average_probabilities[i] * weight_average_probabilities)
        #print(f'Integrated Probability of {emotion}: {average_probabilities[i] * 100:.2f}%')
        # print(f'Integrated Probability of {emotion}: {integrated_probability*100:.2f}%')
    # from numpy.lib.function_base import average
    anxiety_probability = average_probabilities[0] * 100
    anxiety_level_integrated= f"{anxiety_probability:.1f}%"
    # print(anxiety_level_integrated)
    anxiety= float(anxiety_level_integrated.rstrip('%'))
    anxiety=anxiety/100
    return anxiety

#get_anxiety_level()