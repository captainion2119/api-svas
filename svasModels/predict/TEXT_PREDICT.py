import joblib

def predict_depression():
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

    #print(predicted_prob[0][1])
    return f"{predicted_prob[0][1]}"