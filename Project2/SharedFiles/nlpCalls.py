#---------------------------------------------
# File name: nlpCalls.py
# Description: Processes twitter information with tweepy and returns them in lists and dictionaries.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
# Changelog:
# * October 29, 2020 - Changes to google cloud library calls
#---------------------------------------------

# Imports the Google Cloud client library
from google.cloud import language_v1

'''
Initializes the Google NLP API
Input  - None
Output - client, errors
''' 
def init_google_nlp():
    client = None
    errors = []
    try:
        client = language_v1.LanguageServiceClient()
    except :
        errors.append(init_google_nlp.__name__ + ' : Error in initializing the Google Cloud SDK client.')
    
    return (client, errors)


'''
Analyizes a string of text using the Google NLP API
Input  - text: string
Output - sentimentDict:dictionary, errors:list of string
''' 
def analyze_text_sentiment(client, text=''):
    sentimentDict = {}
    sentimentObj = None
    errors = []
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentimentObj = client.analyze_sentiment(request={'document': document}).document_sentiment
    except:
        errors.append(analyze_text_sentiment.__name__ + ': Error with analyzing text sentiment with Google Cloud SDK.')

    if sentimentObj is not None:
        sentimentDict = {"score":sentimentObj.score, "magnitude":sentimentObj.magnitude}
    
    return (sentimentDict,errors)