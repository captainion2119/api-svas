import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import numpy as np

num_classes = 3
emotion_classes = ['Anxiety', 'Sadness', 'Happiness']

batch_size = 16
epochs = 8
input_shape = (224, 224, 3)
learning_rate = 0.0001  # Reduced learning rate for potentially better convergence

example_image_path = 'uploaded/image.png'

def face_predict(case):
    # Load the face model
    face_model = keras.models.load_model('models/face_model_final.h5')
    input_shape = (224, 224, 3)
    img = keras.preprocessing.image.load_img(example_image_path, target_size=input_shape[:2])
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.0  # Preprocess the image
    predictions = face_model.predict(img)

    emotion_index = case - 1
    return f"{predictions[0][emotion_index] * 100:.2f}"

    # for i, emotion in enumerate(emotion_classes):
    #     print(f'Predicted {emotion}: {predictions[0][i] * 100:.2f}%')

# 1 -> anxiety
# 2 -> depression
# 3 -> happiness

# print(face_predict(1))
# print(face_predict(2))
# print(face_predict(3))