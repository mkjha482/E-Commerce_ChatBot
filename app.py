import nltk
#nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import json
import textblob as TextBlob

#read file
myjsonfile = open('Data.json','r')
jsondata = myjsonfile.read()

#parse
obj=json.loads(jsondata)
list = obj['Details']

from keras.models import load_model
model = load_model('model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def chat():
    print("\n\nStart chat with ChatBot Sid\n")
    stre = login()
    if(stre == "True"):
        print("\nSid: Login Successful! Welcome\n")
        while True:
            inp = input("You: ")
            senti(inp)
            if "return" in inp:
                return_item(inp)
            if "buy" in inp:
                product_avail(inp)
            if "purchase" in inp:
                fetch_all(inp)
            if "products" in inp:
                product_name(inp)

            if inp.lower() == 'quit':
                analyse()
                delete_data = open("data.txt", "w")
                delete_data.truncate()
                delete_data.close()
                break

            response = chatbot_response(inp)
            print("\nSid: " + response + '\n')
    else:
        print("\nSid: Wrong credentials. Closing Bot Interface")

def senti(inp):
    outfile = open('data.txt', 'a')
    outfile.write(inp+' ')
    outfile.close()

def analyse():
    infile = open('data.txt', 'r')
    y = str(infile.read())
    print(y)
    edu = TextBlob(y)
    x = edu.sentiment.polarity
    # Negative =x<0 and Neutral =0 and Positive more than 0 and less than 1
    if x < 0:
        print("\nNegative Conversation")
    elif x == 0:
        print("\nNeutral Conversation")
    elif x > 0 and x <= 1:
        print("\nPositive Conversation")
    infile.close()

def login():
    user = "Mayank482"
    passw = "Hello123"
    print("\nSid: Enter username")
    if((input("\nYou: ")) == user):
        print("\nSid: Enter password")
        if((input("\nYou: ")) == passw):
            syt = "True"
    else:
        syt = "False"
    return syt

def product_name(inp):
    print("\nSid: Fetching all products in stock")
    for x in range(len(list)):
        if list[x].get("Availability") != "0":
            pid = list[x].get("Productid")
            pname = list[x].get("ProductName")
            quant = list[x].get("Availability")
            print("\nSid: PID - " + pid + ";  Product Name - " + pname + ";  Quantity in stock - " + quant)

def return_item(inp):
    print("\nSid: Enter order ID")
    set11 = input("\nYou: ")
    for x in range(len(list)):
        if list[x].get("Orderid") == set11:
            print("\nSid: Enter Product ID")
            prdid = input("\nYou: ")
            if list[x].get("Productid") == prdid:
                print("\nSid: Your Customer Name is ", list[x].get("CustomerName"))
                a = input("\n\nSid: Type Yes to confirm\n")
                if a == "Yes" or a == "yes":
                    print("\nSid: Your order will be returned")
                else:
                    print("\nSid: Wrong ID")
            else:
                print("\nSid: Product ID does not match")

def product_avail(inp):
    print("\nSid: Enter Product ID")
    z = input("\nYou: ")
    for x in range(len(list)):
        if list[x].get("Productid") == z:
            if list[x].get("Availability") != "0":
                print("\nProduct available. You can buy it.")
            elif list[x].get("Availability") == "0":
                print("\nProduct unavailable. Apologies")

def fetch_all(inp):
    print("\nSid: Enter your name")
    nme = input("\nYou: ")
    for x in range(len(list)):
        if list[x].get("CustomerName") == nme:
            ido = list[x].get("Orderid")
            pdo = list[x].get("Productid")
            print("\n\nSid: Order ID - " + ido + ";  Product ID - " + pdo)

chat()