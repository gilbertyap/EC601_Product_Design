#---------------------------------------------
# File name: phase2Functions.py
# Description: Processing functions for phase2app.py
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: October 2, 2020
#---------------------------------------------

import configparser, datetime, sys, time
sys.path.insert(1, '..\\SharedFiles\\')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import dates
import nlpCalls, twitterCalls, helper

'''
Initializes both the Twitter and Google Cloud APIs
Input  - twitter_api_key, twitter_api_secret_key: string
Output - twitterApi:tweepy.API, googleClient: google.cloud.language.LanguageServiceClient,errors:list of string
'''
def init_apis(twitter_api_key, twitter_api_secret_key):
    errors = []

    # Initialize Twitter API
    (twitterApi, tweepyErrors) = twitterCalls.init_auth(twitter_api_key, twitter_api_secret_key)
    for err in tweepyErrors:
        errors.append(err)

    # Initialize Google Cloud SDK
    (googleClient, googleErrors) = nlpCalls.init_google_nlp()
    for err in googleErrors:
        errors.append(err)

    return(twitterApi, googleClient, errors)

'''
Input - username:string, startDate:datetime, endDate:datetime
output - (dateList, scoreList, magnitudeList): tuple
'''
def generate_data_lists(twitterApi, googleClient, username, startDate, endDate):
    # Get the desired user profile
    helper.print_with_stars('Getting user profile of @' + str(username))
    (userObj,errors) = twitterCalls.getUserProfile(twitterApi, username)
    if userObj is None:
        errors.append('Please check that the username was correct.')
        return(None, None, None, None, errors)

    helper.console_print('name: ' + str(userObj.name))
    helper.console_print('screen_name: @' + str(userObj.screen_name))
    helper.console_print('')

    startDate = datetime.datetime(startDate.year, startDate.month, startDate.day, 0, 0, 0)
    endDate =   datetime.datetime(endDate.year, endDate.month, endDate.day, 11, 59, 59)

    helper.print_with_stars('Checking for tweets between {} and {}'.format(str(startDate), str(endDate)))
    
    if startDate > endDate:
        errors.append('Start date is after end date! Please repick dates on next run.')
        return(None, None, None, None, errors)

    functionErrorList = []
    (tweetList, errors) = twitterCalls.getTweetsInTimePeriod(twitterApi, username, startDate, endDate)
    if tweetList is None:
        errors.append('Could not get tweets between the dates provided.')
        return(None, None, None, None, errors)

    # twitterCalls.getTweetsInTimePeriod is particularly sensitive to rate limit errors
    # We still want to continue with the tweets we do have, but we need track the non-critical function errors
    if len(errors) > 0:
        for err in errors:
            functionErrorList.append(err)
        functionErrorList.append(generate_data_lists.__name__ + ': There was an error while fetching tweets.')

    if len(tweetList) == 0:
        functionErrorList.append('No tweets retrieved.')
        return(None, None, None, None, functionErrorList)
    else:
        # Switch the order of the list to be oldest to newest
        tweetList.reverse()

        helper.print_with_stars('Analyzing tweets...')

        # Create a dictionary for merging tweets from the same day
        hashDict = {}
        # Create a sentiment score for every tweet and save it
        for tweet in tweetList:
            text = tweet.full_text
            (sentimentDict, errors)= nlpCalls.analyze_text_sentiment(googleClient, text)
            if len(sentimentDict) == 0:
                for error in errors:
                    functionErrorList.append(error)
                functionErrorList.append('Could not generate sentiment for ' + text)
                continue
            else:
                # Create a "hash" of the year+month+day
                hash = '{}-{}-{}'.format(tweet.created_at.year, tweet.created_at.month,tweet.created_at.day)
                try:
                    hashDict[hash][0] += sentimentDict['score']
                    hashDict[hash][1] += sentimentDict['magnitude']
                except:
                    # Create a tuple that is score, magntitude
                    hashDict[hash] = (sentimentDict['score'], sentimentDict['magnitude'])

        # Separate into three lists that for dates, scores, magntitudes
        dateList = []
        scoreList = []
        magnitudeList = []
        for items in hashDict.items():
          dateList.append(items[0])
          scoreList.append(items[1][0])
          magnitudeList.append(items[1][1])

        helper.print_with_stars('Tweet analysis complete!')

    return (dateList, scoreList, magnitudeList, tweetList, functionErrorList)