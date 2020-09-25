#---------------------------------------------
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 24, 2020
#---------------------------------------------

import json, sys
import tweepy

# REMOVE THESE BEFORE PUBLISHING
# API_KEY = ''
# API_SECRET_KEY = ''

'''
Put a comment here
Input  - api and access keys : string
Output - tweepy api object
''' 

def init_auth(apiKey, apiSecretKey):
    # Use OAuth 2 Authentication instead of OAuth 1a
    # Makes API requests for read-only access
    api = None
    errors = []

    if (apiKey == '') or (apiSecretKey == ''):
        errors.append('Keys missing!')
        return (api,errors)

    try:
        auth = tweepy.AppAuthHandler(apiKey, apiSecretKey)
        api = tweepy.API(auth)
    except tweepy.TweepError as err:
        errors.append(init_auth.__name__ + ': ' + str(err))
    return (api,errors)

'''
Gets a page of tweets from a specified user name TODO: Add a parameter for getting more pages of tweets
Input   - username : string
Output  - list of tweet_objects
'''
def getUserTweets(api, username, count=20):
    tweetObjList = []
    errors = []
    
    if count > 200:
      # TODO: errors out for now until you implement paganation
      errors.append('Too many tweets requested. The maximum is 200.')
      return (tweetObjList,errors)
    
    try:
        tweetObjList = api.user_timeline(username)
    except tweepy.TweepError as err:
        errors.append(getUserTweets.__name__ + ': ' + str(err))
    return (tweetObjList,errors)

'''
Gets a user's profile
Input   - username : string
Output  - list of tweet_objects
'''
def getUserProfile(api, username):
    userObj = None
    errors = []
    try:
        userObj = api.get_user(username)
    except tweepy.TweepError as err:
        errors.append(getUserProfile.__name__ + ': ' + str(err))
    return (userObj,errors)

'''
Uses the GET trends/place command. The top 50 trending topics is cached every 5 min and requesting extra will penalize the rate limit.
Input  - 
Output - 
'''
def getTrendingLocations(api):
    locationsList = []
    try:
        locationsJsonObj = api.trends_available()
    except tweepy.TweepError as err:
        errors.append(getTrendingLocations.__name__ + ': ' + str(err))
        return (None, errors)

    for dict in locationsJsonObj:
        if dict['country'] != None:
            country = dict['country']
        
        if dict['name'] != None:
            name = dict['name']
        
        if dict['woeid'] != None:
            woeid = dict['woeid']
        
        locationsList.append({'country' : country, 'name':name, 'woeid': woeid})
    return (locationsList,errors)

def getTrendingTopics(api, woeid):
#      make up 'trends'
#      {
#        'name': '#ChainedToTheRhythm',
#        'url': 'http://twitter.com/search?q=%23ChainedToTheRhythm',
#        'promoted_content': null,
#        'query': '%23ChainedToTheRhythm',
#        'tweet_volume': 48857
#      }
    try:
        trendsJsonObj = api.trends_place(woeid)
    except tweepy.TweepError as err:
        errors.append(getTrendingTopics.__name__ + ': ' + str(err))
        return (None, errors)

    for list in trendsJsonObj:
        if list['trends'] != None:
            trendsList = list['trends']
        
        if list['as_of'] != None:
            as_of = list['as_of']
        
        if list['created_at'] != None:
            created_at = list['created_at']
        
        if list['locations'] != None:
            locationsList = list['locations']

        trendingTopicsDict = {'trends':trendsList, 'as_of':as_of, 'created_at':created_at, 'locations':locationsList}

    return (trendingTopicsDict, errors)

def print_errors(errorList):
    print("Error! See the following errors(s): ")
    for statement in errors:
        print(statement)

if __name__ == '__main__':
    #Authorize API calls
    print('********Testing Twitter API********')
    #if (API_KEY == '') or (API_SECRET_KEY == ''):
    #    print('********Keys missing! Exiting...********')
    #    sys.exit(1)

    [api, errors] = init_auth(API_KEY, API_SECRET_KEY)
    if api is None:
        print_errors(errors)
        sys.exit(1)

    print('********API authenticated. Testing features...********')

    # Get the profile of a user
    username = "BU_tweets"
    print('********Get profile********')
    (userObj,errors) = getUserProfile(api, username)
    if userObj is None:
        print_errors(errors)
        sys.exit(1)
    
    print('name: ' + str(userObj.name))
    print('screen_name: ' + str(userObj.screen_name))
    print('description: ' + str(userObj.description))
    print('url: ' + str(userObj.url))
    print('followers_count: ' + str(userObj.followers_count))
    print('created_at: ' + str(userObj.created_at))
    print('statuses_count : ' + str(userObj.statuses_count))
    print('')
    
    
    # Get the tweets of a user
    print('********Get profile tweets********')
    (userTimelineList,errors) = getUserTweets(api, username)
    
    if userTimelineList is None:
        print_errors(errors)
        sys.exit(1)
    
    for tweet in userTimelineList:
        print('created_at: ' + str(tweet.created_at))
        print('text: ' + str(tweet.text))
        print('source: ' + str(tweet.source))
        print('in_reply_to_user_id: ' + str(tweet.in_reply_to_user_id))
        print('is_quote_status: ' + str(tweet.is_quote_status))
        print('retweet_count: ' + str(tweet.retweet_count))
        print('favorite_count: ' + str(tweet.favorite_count))
        print('')

    # Find trending topic locations
    print('********Getting trending locations...********')
    (locationsList, errors) = getTrendingLocations(api)
    if locationsList is None:
        print_errors(errors)
        sys.exit(1)
    
    
    # Find trending topics in USA
    usa_woeid = 23424977
    print('********Getting trending topics for USA...********')
    (trendingDict, errors) = getTrendingTopics(api, usa_woeid)
    if trendingDict is None:
        print_errors(errors)
        sys.exit(1)
 
    print('********Test complete********')
    sys.exit(0)