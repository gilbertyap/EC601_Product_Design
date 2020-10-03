#---------------------------------------------
# File name: analyzeTwitter.py
# Description: Performs a test on Twitter trending topics and analyzes overall sentinment in ### tweets of the trend.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

import configparser, sys, time
sys.path.insert(1, '..\\SharedFiles\\')
import nlpCalls, twitterCalls, helper

SETTINGS_FILE = '..\\SharedFiles\\settings.ini'

'''
Initializes both the Twitter and Google Cloud APIs
Input  - twitter_api_key, twitter_api_secret_key: string
Output - twitterApi:tweepy.API, googleClient: google.cloud.language.LanguageServiceClient,errors:list of string
'''
def init_apis(twitter_api_key, twitter_api_secret_key):
    errors = []
    
    # Initialize Twitter API
    (twitterApi, tweepyErrors) = twitterCalls.init_auth(twitter_api_key, twitter_api_secret_key)

    # Initialize Google Cloud SDK
    (googleClient, googleErrors) = nlpCalls.init_google_nlp()

    # Exit if errors found with the initialization process
    errors = tweepyErrors + googleErrors

    return(twitterApi, googleClient, errors)

'''
Gets a list of tweets of most popular tweets from a query and also saves the most retweeted tweet that matches that query
Input  - twitterApi:tweepy.API, query: string, numSearchResults:int
Output - topTrendTweetList:list of tweepy.Status, topRtTweet:tweepy.Status, errors:list of string
'''
def getTweetsFromQuery(twitterApi, query, numSearchResults):
    topTrendTweetList = None
    topRtTweet = None
    errors = []

    (searchResultTweetList, errors) = twitterCalls.doSearch(twitterApi, query, numSearchResults, 'popular')
    if searchResultTweetList is None:
        return (topTrendTweetList, topRtTweet, errors)

    # Go through the list of statuses, get their id, get the full tweet text, and then append to topTrendTweetList
    topTrendTweetList = []
    topRtCount = 0
    topRtTweet = None
    for status in searchResultTweetList:
        (fullTweetObj,errors) = twitterCalls.getTweet(twitterApi, status.id)
        if fullTweetObj is None:
            return (None, topRtTweet, errors)

        if fullTweetObj.retweet_count > topRtCount:
            topRtTweet = fullTweetObj
            topRtCount = fullTweetObj.retweet_count
        topTrendTweetList.append(fullTweetObj.full_text)
    
    return (topTrendTweetList, topRtTweet, errors)

'''
Uses the Google Cloud NLP API to analyze a list of strings
Input  - textList: list of string
Output - listScore:float, listMagnitude:float
'''
def analyzeTextList(textList):
    # Go through the textList and generate a score and magnitude for the entire list
    listScore = 0
    listMagnitude = 0
    for text in textList:
        (sentimentDict,errors) = nlpCalls.analyze_text_sentiment(googleClient, text)

        if len(sentimentDict) == 0:
            helper.console_print('Could not generate sentiment for ' + text)
            helper.print_errors(errors)
            continue
        else:
            listScore += sentimentDict['score'] 
            listMagnitude += sentimentDict['magnitude']
        
        # Wait one second between Google Queries
        time.sleep(0.5)

    return (listScore, listMagnitude)

if __name__ == '__main__':
    # start_time = time.time()

    # Read the SETTINGS_FILE
    settings = configparser.ConfigParser()
    settings.read(SETTINGS_FILE)
    numSearchResults  = 50

    # Initialize APIs
    helper.print_with_stars('Initializing APIs')
    (twitterApi, googleClient, errors) = init_apis(settings['KEYS']['api_key'], settings['KEYS']['api_secret_key'])
    
    if(len(errors) != 0):
        helper.print_errors(errors)
        helper.console_print('Please check that your keys are added into the \'settings.ini\' file.')
        sys.exit(1)

    # Get the top trends in United States
    helper.print_with_stars('Getting top trending hashtag for USA')
    usaWoeid = 23424977
    (trendingDict, errors) = twitterCalls.getTrendingTopics(twitterApi, usaWoeid)
    if trendingDict is None:
        helper.print_errors(errors)
        sys.exit(1)

    # Find the trending hashtag with the highest tweet volume
    topTrendName = ''
    topTweetVolume = 0
    for trend in trendingDict['trends']:
        if (trend['tweet_volume'] is not None):
            if ('%23' in trend['query']) and (trend['tweet_volume'] > topTweetVolume):
                if trend['name'] != None:
                    topTrendName = trend['name']

                if trend['tweet_volume'] != None:
                    topTweetVolume = trend['tweet_volume']

    helper.console_print('Top trending hastag is: ' + topTrendName +'\n')

    helper.print_with_stars('Analyzing popular tweets in ' + topTrendName)
    helper.console_print('Processing tweets...')

    (trendList, topRtTweet, errors) = getTweetsFromQuery(twitterApi, topTrendName, numSearchResults)
    if trendList is None:
        helper.print_errors(errors)
        sys.exit(1)

    # Go through the trendList and generate a score and magnitude for the entire list
    helper.console_print('Processing may take a minute or two...\n')
    (listScore, listMagnitude) = analyzeTextList(trendList)

    # Print out information 
    helper.print_with_stars('Analysis complete')
    helper.console_print('Top trending #hashtag in USA: ' + str(topTrendName))
    helper.console_print('Sentiment of '  + str(topTrendName) +': score=' + str(listScore) + ', magnitude=' + str(listMagnitude))
    helper.console_print('Average Sentiment of '  + str(topTrendName) +': score=' + str(listScore/numSearchResults) + ', magnitude=' + str(listMagnitude/numSearchResults))
    helper.console_print("Most retweeted message with {} is by user {} with {} retweets. Text: {}".format(str(topTrendName), topRtTweet.user.screen_name, topRtTweet.retweet_count, topRtTweet.full_text))
    helper.console_print()

    # helper.console_print('Execution time was ' + str(time.time() - start_time) + ' seconds.')
    # helper.console_print()

    # Generate a list of sentiment score averages for the trending topics
    helper.print_with_stars('Analyzing sentiment scores of other trending hashtags...')
    helper.console_print('This will take several minutes...')
    sentimentEvaluationList = []
    for trend in trendingDict['trends']:
        if (trend['tweet_volume'] is not None):
            if ('%23' in trend['query']):
                (trendList, topRtTweet, errors) = getTweetsFromQuery(twitterApi, trend['name'], numSearchResults)
                if trendList is None:
                    helper.print_errors(errors)
                    continue

                (listScore, listMagnitude) = analyzeTextList(trendList)

                # Add the score and magnitude tuples to a list
                sentimentEvaluationList.append((trend['name'], listScore,listMagnitude))

    helper.print_with_stars('Other trending hastags and their scores')
    for (trendName, trendScore, trendMagnitude) in sentimentEvaluationList:
        helper.console_print('Name {}, Score {}, Magnitude {}'.format(str(trendName), str(trendScore), str(trendMagnitude)))

    helper.console_print()
    sys.exit(0)