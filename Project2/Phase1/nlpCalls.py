#---------------------------------------------
# File name: nlpCalls.py
# Description: Processes twitter information with tweepy and returns them in lists and dictionaries.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import sys

from helper import print_errors

'''
Put a comment here
Input  - None
Output - client, errors
''' 
def init_google_nlp():
    client = None
    errors = []
    try:
        client = language.LanguageServiceClient()
    except :
        errors.append(init_google_nlp.__name__ + ' : Error in initializing the Google Cloud SDK client.')
    
    return (client, errors)


'''
Put a comment here
Input  - text: string
Output - sentimentDict, errors
''' 
def analyze_text_sentiment(client, text=''):
    sentimentDict = {}
    sentimentObj = None
    errors = []
    try:
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentimentObj = client.analyze_sentiment(document=document).document_sentiment
    except:
        errors.append(analyze_text_sentiment.__name__ + ': Error with analyzing text sentiment with Google Cloud SDK.')

    if sentimentObj is not None:
        sentimentDict = {"score":sentimentObj.score, "magnitude":sentimentObj.magnitude}
    
    return (sentimentDict,errors)

if __name__ == '__main__':
    (client, errors) = init_google_nlp()
    if client is None:
        print_errors(errors)
        sys.exit(1)
    
    # The text to analyze
    text = u'Hello, world!'
    (sentimentDict,errors) = analyze_text_sentiment(text)
    if len(sentimentDict) == 0:
        print_errors(errors)
        sys.exit(1)

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentimentDict['score'], sentimentDict['magnitude']))
    
    sys.exit(0)