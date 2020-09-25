#---------------------------------------------
# File name: analyzeTwitter.py
# Description: Performs a test on Twitter trending topics and analyzes overall sentinment in ### tweets of the trend.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

import configparser, sys, time
import nlpCalls, twitterCalls, helper

SETTINGS_FILE = 'settings.ini'

'''
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
'''
def getTweetsFromQuery(twitterApi, query, numSearchResults):
    # Perform a Twitter search against the top hastag query
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
'''
def analyzeTextList(textList):
    # Go through the textList and generate a score and magnitude for the entire list
    listScore = 0
    listMagnitude = 0
    for text in textList:
        (sentimentDict,errors) = nlpCalls.analyze_text_sentiment(googleClient, text)

        if len(sentimentDict) == 0:
            print('Could not generate sentiment for ' + text)
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
    numSearchResults  = int(settings['SEARCH']['numSearchResults'])

    # Initialize APIs
    helper.print_with_stars('Initializing APIs')
    (twitterApi, googleClient, errors) = init_apis(settings['KEYS']['api_key'], settings['KEYS']['api_secret_key'])
    
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

    print('Top trending hastag is: ' + topTrendName +'\n')

    helper.print_with_stars('Analyzing popular tweets in ' + topTrendName)
    print('Processing tweets...')

    (trendList, topRtTweet, errors) = getTweetsFromQuery(twitterApi, topTrendName, numSearchResults)
    if trendList is None:
        helper.print_errors(errors)
        sys.exit(1)

    # Go through the trendList and generate a score and magnitude for the entire list
    print('Processing may take a minute or two...\n')
    (listScore, listMagnitude) = analyzeTextList(trendList)

    # Print out information 
    helper.print_with_stars('Analysis complete')
    print('Top trending #hashtag in USA: ' + str(topTrendName))
    print('Sentiment of '  + str(topTrendName) +': score=' + str(listScore) + ', magnitude=' + str(listMagnitude))
    print('Average Sentiment of '  + str(topTrendName) +': score=' + str(listScore/numSearchResults) + ', magnitude=' + str(listMagnitude/numSearchResults))
    print("Most retweeted message with {} is by user {} with {} retweets. Text: {}".format(str(topTrendName), topRtTweet.user.screen_name, topRtTweet.retweet_count, topRtTweet.full_text))
    print()

    # print('Execution time was ' + str(time.time() - start_time) + ' seconds.')
    # print()

    # Generate a list of sentiment score averages for the trending topics
    helper.print_with_stars('Analyzing sentiment scores of other trending hashtags...')
    print('This will take several minutes...')
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
        print('Name {}, Score {}, Magnitude {}'.format(str(trendName), str(trendScore), str(trendMagnitude)))

    print()
    sys.exit(0)