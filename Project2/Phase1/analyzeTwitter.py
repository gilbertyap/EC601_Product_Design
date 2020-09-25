#---------------------------------------------
# File name: analyzeTwitter.py
# Description: Performs a test on Twitter trending topics and analyzes overall sentinment in ### tweets of the trend.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

import sys, time
import nlpCalls, twitterCalls, helper

# REMOVE THESE BEFORE PUBLISHING
API_KEY = ''
API_SECRET_KEY = ''

def init_apis():
    errors = []
    # Initialize Twitter API
    (twitterApi, tweepyErrors) = twitterCalls.init_auth(API_KEY, API_SECRET_KEY)

    # Initialize Google Cloud SDK
    (googleClient, googleErrors) = nlpCalls.init_google_nlp()

    # Exit if errors found with the initialization process
    errors = tweepyErrors + googleErrors

    return(twitterApi, googleClient, errors)

if __name__ == '__main__':
    numSearchResults = 50

    # Initialize APIs
    helper.print_with_stars('Initializing APIs')
    (twitterApi, googleClient, errors) = init_apis()
    if(len(errors) != 0):
        helper.print_errors(errors)
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

    helper.print_with_stars('Top trending hastag is: ' + topTrendName)

    helper.print_with_stars('Analyzing popular tweets in ' + topTrendName)

    # Perform a Twitter search against the top hastag query
    (searchResultTweetList, errors) = twitterCalls.doSearch(twitterApi, topTrendName, numSearchResults, 'popular')
    if searchResultTweetList is None:
        helper.print_errors(errors)
        sys.exit(1)

    # Go through the list of statuses, get their id, get the full tweet text, and then append to topTrendTweetList
    topTrendTweetList = []
    topRtCount = 0
    topRtTweet = None
    for status in searchResultTweetList:
        (fullTweetObj,errors) = twitterCalls.getTweet(twitterApi, status.id)
        if fullTweetObj is None:
            helper.print_errors(errors)
            sys.exit(1)

        if fullTweetObj.retweet_count > topRtCount:
            topRtCount = fullTweetObj.retweet_count
            topRtTweet = fullTweetObj
        topTrendTweetList.append(fullTweetObj.full_text)

    # Go through the topTrendTweetList and generate a score and magnitude for the entire list
    listScore = 0
    listMagnitude = 0
    for tweetText in topTrendTweetList:
        (sentimentDict,errors) = nlpCalls.analyze_text_sentiment(googleClient, tweetText)

        if len(sentimentDict) == 0:
            print('Could not generate sentiment for ' + tweetText)
            helper.print_errors(errors)
            continue
        else:
            listScore += sentimentDict['score'] 
            listMagnitude += sentimentDict['magnitude']
        
        # Wait one second between Google Queries
        time.sleep(1)

    # Print out information 
    helper.print_with_stars('Analysis complete')
    print('Top trending #hashtag in USA: ' + str(topTrendName))
    print('Sentiment of '  + str(topTrendName) +': score=' + str(listScore) + ', magnitude=' + str(listMagnitude))
    print('Average Sentiment of '  + str(topTrendName) +': score=' + str(listScore/100) + ', magnitude=' + str(listMagnitude/100))
    print("Most retweeted tweet of {} is by user {} with {} retweets. Text: {}".format(str(topTrendName), topRtTweet.user.screen_name, topRtTweet.retweet_count, topRtTweet.full_text))
    
    sys.exit(0)