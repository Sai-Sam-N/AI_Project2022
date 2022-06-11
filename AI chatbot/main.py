import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import names #random name generator
from tensorflow.keras.models import load_model


lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("\n\n|============= Welcome to Hospital Appointment Chatbot System! =============|")
print("|================================= Feel Free ===============================|")
print("|===================================== To ==================================|")
print("|============================== chat with KHAVS ============================|")

Questions_to_ask = ["Hii, how can we help you? Please list out your symptoms : ",
                    "Please give us your details such as name, age, phone number separated by ',' ",
                    "Would you like to add anything else? (y/n) ",
                    "Thank you, hope you get well soon. We will notify you with the details of your "
                                  "appointment at the earliest"]

numques = len(Questions_to_ask)

#File to save the symptoms
f = open("patient_details.txt", "w+")
contents = []

for i in range(numques):

    if (i == 1) or (i == 2):
        print("| Bot:", Questions_to_ask[i])
        message = input("| You: ")
        contents.append(message)
        message = message.lower()
        if (i == 2) and (message == "y" or message == "Y" or message == "Yes" or message == "yes"):
            print("| Bot: Please specify")
            message = input("| You: ")
            contents.append(message)
            message = message.lower()
        elif (i == 2):
            pass
        print("\n")
    elif i != numques-1:
        print("| Bot:", Questions_to_ask[i])
        message = input("| You: ")
        contents.append(message)
        message = message.lower()
        ints = predict_class(message)
        res = get_response(ints, intents)
        print("| Bot:", res)
        print("\n")
    else:
        print("| Bot:", Questions_to_ask[i])
        doc_name = names.get_full_name()
        # print("\n\tAppointment details\nDr.", doc_name, " at 6:30pm.\nLocation - KHAVS Hospital, Khavsapuram")
        # print("\n\tAppointment details\nDr.", doc_name, " at 6:30pm.\nLocation - Apollo Hospitals, Kodambakkam")
        # print("\n\tAppointment details\nDr.", doc_name, " at 6:30pm.\n")
        # exit()

# Processing the data
contents.pop(2)
lst = contents[1].split(",")
contents[1] = lst

# Details of the Patient to the file
f.write(f"\nName : {contents[1][0]}")
f.write(f"\nAge : {contents[1][1]}")
f.write(f"\nPhone number : {contents[1][2]}")
f.write("\nDetails : \n")
f.write(contents[0])
f.write("\n")
if(contents[2]):
    f.write(contents[2])
f.close() # closing the file

# Location

# Getting the user's device name and IP Address
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(f"\nUser's device name is : {hostname}")
print(f"User's IP Address is : {IPAddr}\n")


# Hospitals dataset
import pandas as pd

hs_dataset = pd.read_csv("Hospital.csv")
hs_dataset.head()

# Fetching the required columns
hs_new = hs_dataset[['NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'WEBSITE', 'LATITUDE', 'LONGITUDE']].copy()
hs_new.head()

# Renaming the column names
hs_new=hs_new.rename(columns={'LATITUDE': 'LAT', 'LONGITUDE': 'LON'})

import math
def Dist(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def MinIndex(d):
  min = 1000
  index = 0
  for i in range(len(d)):
    if (min > d[i]):
      min = d[i]
      index = i
  return index

def FindDist(la, lo):
  dist = []
  for i in range(len(hs_new)):
    plat = hs_new['LAT'][i]
    plon = hs_new['LON'][i]
    d = Dist(la,lo,plat,plon)
    dist.append(d)
  ind = MinIndex(dist)

  # Printing the nearest hospital
  print("\n\tAppointment details\nDr.", doc_name, " at 6:30pm.\n")
  print(f"\nHospital Name : \n{hs_new['NAME'][ind]}")
  print(f"\n\nHospital Address : \n{hs_new['ADDRESS'][ind]},{hs_new['CITY'][ind]},{hs_new['STATE'][ind]} - {hs_new['ZIP'][ind]}")
  print(f"\n\nHospital Website : {hs_new['WEBSITE'][ind]}")
  # print(dist)

latitude = 24
longitude = 20
FindDist(latitude, longitude)