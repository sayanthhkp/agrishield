# import json
# import string
# import random
# import nltk
# import numpy as num
# from nltk.stem import WordNetLemmatizer # It has the ability to lemmatize.
# import tensorflow as tensorF # A multidimensional array of elements is represented by this symbol.
# from tensorflow.keras import Sequential # Sequential groups a linear stack of layers into a tf.keras.Model
# from tensorflow.keras.layers import Dense, Dropout
#
# # nltk.download("punkt")# required package for tokenization
# # nltk.download("wordnet")# word database
# # nltk.download('omw-1.4')
#
# from tensorflow.python.keras.saving import load_model
#
#
# static_path=r"C:\Users\alen kurian\PycharmProjects\agrishiled\myapp\static\chatbot\\"
# data_file = open(static_path+ 'Data.json').read()
# data = json.loads(data_file)
# # print("Data : \n",data)
#
# lm = WordNetLemmatizer() #reducing words to their base or dictionary form
# ourClasses = []
# newWords = []
# documentX = []
# documentY = []
# # Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
# for intent in data["ourIntents"]:
#     for pattern in intent["patterns"]:
#         ournewTkns = nltk.word_tokenize(pattern)
#         newWords.extend(ournewTkns)
#         documentX.append(pattern)
#         documentY.append(intent['tag'])
#     if intent["tag"] not in ourClasses:
#         ourClasses.append(intent["tag"])
#
# newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in string.punctuation]
# newWords = sorted(set(newWords))
# ourClasses = sorted(set(ourClasses))
#
# trainingData  = []
# outEmpty = [0] * len(ourClasses)
#
# for idx, doc in enumerate(documentX):
#     bag0words = []
#     text = lm.lemmatize(doc.lower())
#     for word in newWords :
#         bag0words.append(1) if word in text else bag0words.append(0)
#
#     outputRow = list(outEmpty)
#     outputRow[ourClasses.index(documentY[idx])] = 1
#     trainingData.append([bag0words, outputRow])
#
# random.shuffle(trainingData)
# trainingData = num.array(trainingData, dtype=object)
#
# x = num.array(list(trainingData[:,0]))
# y = num.array(list(trainingData[:,1]))
#
# iShape = (len(x[0]),)
# oShape = len(y[0])
#
# ###########         Training
# # Model = Sequential()
# # Model.add(Dense(128, activation="relu" , input_shape=iShape))
# # Model.add(Dropout(0.5)) #Dropout is a regularization technique that randomly drops out (sets to zero) some of the inputs to a layer during training to prevent overfitting.
# # Model.add(Dense(64, activation="relu"))
# # Model.add(Dropout(0.3))
# # Model.add(Dense(oShape, activation='softmax'))
# # md = tensorF.keras.optimizers.Adam(learning_rate= 0.01)
# # Model.compile(optimizer=md, loss='categorical_crossentropy', metrics=['accuracy'])
# # print(Model.summary())
# # Model.fit(x,y, epochs=200, verbose=1)
# # Model.save(static_path + "model.h5")
# ##########      Training end
#
# def ourText(text):
#   newtkns = nltk.word_tokenize(text)
#   newtkns = [lm.lemmatize(word) for word in newtkns]
#   return newtkns
#
# def wordBag(text, vocab):
#   newtkns = ourText(text)
#   bagOwords = [0] * len(vocab)
#   for w in newtkns:
#     for idx, word in enumerate(vocab):
#       if word == w:
#         bagOwords[idx] = 1
#   return num.array(bagOwords)
#
# def Pclass(text, vocab, labels):
#   Model=load_model(static_path + "model.h5")
#   bagOwords = wordBag(text, vocab)
#   ourResult = Model.predict(num.array([bagOwords]))[0]
#   newThresh = 0.2
#   yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]
#   yp.sort(key=lambda x: x[1], reverse=True)
#   newList = []
#   for r in yp:
#     newList.append(labels[r[0]])
#   print("Txt  ", newList)
#   return newList
#
# def getRes(firstlist, fJson):
#   tag = firstlist[0]
#   listOfIntents = fJson["ourIntents"]
#   for i in listOfIntents:
#     if i["tag"] == tag:
#       ourResult = random.choice(i["responses"])
#       break
#   return ourResult
#
#
# def get_response(msg):
#     intents = Pclass(msg, newWords, ourClasses)
#     ourResult = getRes(intents, data)
#     print(ourResult)
#     return ourResult
#
#


import json
import string
import random
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer
import tensorflow as tensorF
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.models import load_model
import pickle
import os

# Download required NLTK data
# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download('omw-1.4')

static_path = r"/Users/siva/Desktop/To get a job/Agri-ai/agri-web/myapp/static/chatbot//"
data_file = open(static_path + 'Data.json').read()
data = json.loads(data_file)

lm = WordNetLemmatizer()
ourClasses = []
newWords = []
documentX = []
documentY = []

# Tokenization and preprocessing
for intent in data["ourIntents"]:
    for pattern in intent["patterns"]:
        ournewTkns = nltk.word_tokenize(pattern)
        newWords.extend(ournewTkns)
        documentX.append(pattern)
        documentY.append(intent['tag'])
    if intent["tag"] not in ourClasses:
        ourClasses.append(intent["tag"])

# Optimized lemmatization with set for faster lookup
punctuation_set = set(string.punctuation)
newWords = [lm.lemmatize(word.lower()) for word in newWords if word not in punctuation_set]
newWords = sorted(set(newWords))
ourClasses = sorted(set(ourClasses))

# Save preprocessed data for faster loading
pickle.dump(newWords, open(static_path + 'words.pkl', 'wb'))
pickle.dump(ourClasses, open(static_path + 'classes.pkl', 'wb'))

# Optimized bag of words creation
trainingData = []
outEmpty = [0] * len(ourClasses)

# Create word index lookup for O(1) access
word_index = {word: idx for idx, word in enumerate(newWords)}

for idx, doc in enumerate(documentX):
    bag0words = [0] * len(newWords)
    # Tokenize and lemmatize each word in the pattern
    text_words = [lm.lemmatize(word.lower()) for word in nltk.word_tokenize(doc)]

    # Use word index for faster lookup
    for word in text_words:
        if word in word_index:
            bag0words[word_index[word]] = 1

    outputRow = list(outEmpty)
    outputRow[ourClasses.index(documentY[idx])] = 1
    trainingData.append([bag0words, outputRow])

random.shuffle(trainingData)
trainingData = num.array(trainingData, dtype=object)

x = num.array(list(trainingData[:, 0]))
y = num.array(list(trainingData[:, 1]))

iShape = (len(x[0]),)
oShape = len(y[0])

###########  OPTIMIZED TRAINING MODEL
# Model = Sequential()
# # Optimized architecture
# Model.add(Dense(256, activation="relu", input_shape=iShape))
# Model.add(BatchNormalization())  # Faster convergence
# Model.add(Dropout(0.5))
# Model.add(Dense(128, activation="relu"))
# Model.add(BatchNormalization())
# Model.add(Dropout(0.4))
# Model.add(Dense(64, activation="relu"))
# Model.add(Dropout(0.3))
# Model.add(Dense(oShape, activation='softmax'))
#
# # Optimized optimizer
# md = tensorF.k eras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999)
# Model.compile(optimizer=md, loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Callbacks for better training
# early_stop = EarlyStopping(monitor='loss', patience=20, restore_best_weights=True)
# reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=10, min_lr=0.00001)
#
# print(Model.summary())
#
# # Train with callbacks and batch processing
# Model.fit(x, y, epochs=200, verbose=1, batch_size=8, callbacks=[early_stop, reduce_lr])
# Model.save(static_path + "model.h5")
##########  TRAINING END

# Cache model globally to avoid reloading
_cached_model = None


def get_model():
    global _cached_model
    if _cached_model is None:
        _cached_model = load_model(static_path + "model.h5")
    return _cached_model


# Optimized text preprocessing
def ourText(text):
    newtkns = nltk.word_tokenize(text.lower())  # Lowercase once
    newtkns = [lm.lemmatize(word) for word in newtkns]
    return newtkns


# Optimized bag of words with word index
def wordBag(text, vocab):
    newtkns = ourText(text)
    bagOwords = [0] * len(vocab)

    # Use set for O(1) lookup
    token_set = set(newtkns)
    for idx, word in enumerate(vocab):
        if word in token_set:
            bagOwords[idx] = 1

    return num.array(bagOwords)


# Optimized prediction
def Pclass(text, vocab, labels):
    Model = get_model()  # Use cached model
    bagOwords = wordBag(text, vocab)

    # Single prediction is faster than batch
    ourResult = Model.predict(num.array([bagOwords]), verbose=0)[0]

    # Optimized threshold filtering
    newThresh = 0.25  # Slightly higher for better accuracy
    yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]

    if not yp:  # Fallback if no predictions above threshold
        yp = [[num.argmax(ourResult), num.max(ourResult)]]

    yp.sort(key=lambda x: x[1], reverse=True)
    newList = [labels[r[0]] for r in yp]

    print("Predicted tags:", newList)
    return newList


# Cached intent lookup
_intent_cache = {}


def getRes(firstlist, fJson):
    if not firstlist:
        return "I'm not sure I understand. Can you rephrase?"

    tag = firstlist[0]

    # Use cache
    if tag in _intent_cache:
        return random.choice(_intent_cache[tag])

    # Build cache
    for i in fJson["ourIntents"]:
        _intent_cache[i["tag"]] = i["responses"]

    return random.choice(_intent_cache.get(tag, ["I'm not sure how to respond to that."]))


def get_response(msg):
    intents = Pclass(msg, newWords, ourClasses)
    ourResult = getRes(intents, data)
    print(ourResult)
    return ourResult