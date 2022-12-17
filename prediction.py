import pickle
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences

import nltk
import spacy
import string
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
stop_words = set(stopwords.words("english"))


#loading tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

skill_prediction_model = load_model('skill_prediction.h5')
job_predictor_model = load_model('job_predictor.h5')

# loading vectorizer and tokenizer

with open('vectorizer.pickle', 'rb') as handle:
    vectorizer = pickle.load(handle)

with open('LabelEncoder.pickle', 'rb') as handle:
    LabelEncoder = pickle.load(handle)

def predict(model,tokenizer,word):
    input = pad_sequences(tokenizer.texts_to_sequences([word]),maxlen=20)
    # input = tokenizer.texts_to_sequences([word])
    d = model.predict(input)
    # print('probebilty ',d)
    if d <= 0.5:
        d = 0 #'non skill word'
    else:
        d = 1 #'skill word' 
    return d

#Initializing the spacy engine and then use it to process the text:
nlp = spacy.load('en_core_web_sm')

# remove stopwords function
def remove_stopwords(text):
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    r = TreebankWordDetokenizer().detokenize(filtered_text)
    return r

# remove punctuation
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def text_preprocess(text):
    r = text.lower() # coverting into lower case
    r = remove_stopwords(r) # removing stop words
    r = re.sub(r'\d+', '', r) # removing numbers
    r = remove_punctuation(r) # removing punctuations
    r = " ".join(r.split()) # removing white sapce
    r = ''.join(r.splitlines()) # removing newline character
    return r

# function for the predicting job title
import numpy as np
import matplotlib.pyplot as plt

def predict_title(text):
    nouns = []
    doc = nlp(text.lower()) # lowercase
    for chunk in doc.noun_chunks: # extracting nouns from the text input
        chunk = text_preprocess(str(chunk))
        nouns.append(chunk)
    dir_temp = dict()
    for i in nouns:
        # print(type(i))
        r = predict(skill_prediction_model,tokenizer,i) # predicting skill words using Our LSTM model
        if r == 1:
          dir_temp[i] = r
    print(list(dir_temp.keys())) # printing extracted skill words
    data = str(list(dir_temp.keys())) 
    print(type(data))
    vec_data = vectorizer.transform([data]) # vectorizing the skill words
    pred = job_predictor_model.predict(vec_data) # predicting the job title
    print(pred)
    title = np.argmax(pred,axis=1) # taking highest percentage

    best_title = LabelEncoder.inverse_transform(title)
    titles = LabelEncoder.classes_

    return best_title,pred[0],titles
    