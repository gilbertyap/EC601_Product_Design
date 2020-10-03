#---------------------------------------------
# File name: twitterCalls.py
# Description: Processes twitter information with tweepy and returns them in lists and dictionaries.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 24, 2020
#---------------------------------------------

import configparser, datetime, json, sys
import tweepy
import helper

SETTINGS_FILE = 'settings.ini'

'''
Initializes the Twitter API using OAuth 2 (Read-Only)
Input  - api,apiSecretKey: string
Output - api:tweepy.API, errors:list of string
''' 
def init_auth(apiKey, apiSecretKey):
    # Use OAuth 2 Authentication instead of OAuth 1a
    # Makes API requests for read-only access
    api = None
    errors = []

    if (apiKey == '') or (apiSecretKey == ''):
        errors.append(init_auth.__name__ + ': Keys missing from settings.ini file in \'SharedFiles\' folder!')
        return (api,errors)

    try:
        auth = tweepy.AppAuthHandler(apiKey, apiSecretKey)
        api = tweepy.API(auth)
    except tweepy.TweepError as err:
        errors.append(init_auth.__name__ + ': ' + str(err))
    return (api,errors)

'''
Gets a page of tweets from a specified user name TODO: Add a parameter for getting more pages of tweets
Input   - api:tweepy.API, username:string
Output  - tweetObj:tweepy.Status, errors:list of string
'''
def getTweet(api, id):
    tweetObj = None
    errors = []

    try:
        tweetObj = api.get_status(id, tweet_mode='extended')
    except tweepy.TweepError as err:
        errors.append(init_auth.__name__ + ': ' + str(err))

    return (tweetObj,errors)

'''
Gets the most popular tweets from a search
Input   - api:tweepy.API, username:string
Output  - statusList:list of tweepy.Status, errors:list of string
'''
def doSearch(api, query, count=100, result_type='mixed'):
    statusList = None
    errors = []

    try:
        # Only get English results since 
        searchResults = api.search(query, lang='en', count=count, result_type=result_type)
    except tweepy.TweepError as err:
        errors.append(doSearch.__name__ + ': ' + str(err))

    if len(searchResults) == 0:
        errors.append(doSearch.__name__ + ': ' + 'Could not get results for search term \"'+ query +'\"')
    else:
        statusList = []
        for result in searchResults:
            statusList.append(result)

    return (statusList,errors)

'''
Gets a page of tweets from a specified user name TODO: Add a parameter for getting more pages of tweets
Input   - api:tweepy.API, username:string
Output  - tweetObjList,tweepy.StatuList, errors:list of string
'''
def getUserTimeline(api, username, count=20, max_id=-1):
    tweetObjList = None
    errors = []
    
    if count > 200:
      # TODO: errors out for now until you implement paganation
      errors.append('Too many tweets requested. The maximum is 200.')
      return (tweetObjList,errors)
    
    try:
        if max_id != -1:
            tweetObjList = api.user_timeline(screen_name=username, count=count, max_id=max_id)
        else:
            tweetObjList = api.user_timeline(screen_name=username, count=count)
    except tweepy.TweepError as err:
        errors.append(getUserTimeline.__name__ + ': ' + str(err))
    return (tweetObjList,errors)

'''
Gets a user's profile
Input   - api:tweepy.API,tweepyusername:string
Output  - userObj:tweepy.User, errors:list of string
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
Returns as many tweets as possible between the two dates. Optional "textOnly" input that will only get the tweet text.
Input   - api, username:string, startDate:datetime, endDate:datetime, textOnly:boolean
Output  - tweetList:list of tweepy.Status or list of string, errors:list of string
'''
def getTweetsInTimePeriod(api, username, startDate, endDate, textOnly=False):
    tweetList = []
    errors = []

    # To be most efficient, we start at the most recent tweets and work our way to the oldest tweets
    # This will minimize the number of Twitter Api GET user_timeline calls
    # TODO - Determine the optimal count value so that too many tweets aren't fetched when they don't need to be
    try:
        continueSearching = True
        userTimelineCursor = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=False, count=50)
        helper.console_print('Acquired first set of tweets...')
        while(continueSearching):
            continueReadingPages = True
            for page in userTimelineCursor.pages():
                for status in page:
                    if (status.created_at >= startDate):
                        if (status.created_at < endDate):
                            (fullStatus, fetchErrors) = getTweet(api, status.id)
                            if fullStatus is not None:
                                if(textOnly):
                                    tweetList.append(fullStatus.full_text)
                                else:
                                    tweetList.append(fullStatus)
                            else:
                                # Check errors for a rate limit issue. You want to return at this point if you find a rate limit error.
                                for error in fetchErrors:
                                    if 'rate limit' in error.lower():
                                        errors.append(getTweetsInTimePeriod.__name__ + ': Error! Rate limit was reached. Try waiting 15 minutes. If that does not work, you may need to wait 24 hours.')
                                        return(tweetList, errors)
                                    else:
                                        helper.console_print('Error! Could not get the full tweet for status.id ' + str(status.id))
                    else:
                        continueReadingPages = False
                        break

                if (page[len(page)-1].created_at > startDate) and (continueReadingPages):
                    helper.console_print('Getting more tweets...last date was ' + str(page[len(page)-1].created_at))
                    userTimelineCursor = tweepy.Cursor(api.user_timeline, screen_name=username, count=100, max_id=page[len(page)-1].id)
                elif (not continueReadingPages):
                    break

            if(not continueReadingPages):
                continueSearching = False

    except tweepy.TweepError as err:
        errors.append(getTweetsInTimePeriod.__name__ + ': ' + str(err))
        return (None, errors)

    return (tweetList, errors)

'''
Uses the GET trends/place command. The top 50 trending topics is cached every 5 min and requesting extra will penalize the rate limit.
Input  - api:tweepy.API
Output - locationsList:dictionary, errors:list of string
'''
def getTrendingLocations(api):
    locationsList = None
    try:
        locationsJsonObj = api.trends_available()
    except tweepy.TweepError as err:
        errors.append(getTrendingLocations.__name__ + ': ' + str(err))
        return (None, errors)

    if locationsJsonObj is not None:
        locationsList = []
        for dict in locationsJsonObj:
            if dict['country'] != None:
                country = dict['country']
            
            if dict['name'] != None:
                name = dict['name']
            
            if dict['woeid'] != None:
                woeid = dict['woeid']
            
            locationsList.append({'country' : country, 'name':name, 'woeid': woeid})
    return (locationsList,errors)

'''
Uses the GET trends/place command. The top 50 trending topics is cached every 5 min and requesting extra will penalize the rate limit.
Input  - api:tweepy.API, woeid:int
Output - trendingTopicsDict:dictionary, errors:list of string
'''
def getTrendingTopics(api, woeid):
    trendingTopicsDict = None
    errors = []

    try:
        trendsJsonObj = api.trends_place(woeid)
    except tweepy.TweepError as err:
        errors.append(getTrendingTopics.__name__ + ': ' + str(err))
        return (None, errors)
    
    if trendsJsonObj is not None:
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

if __name__ == '__main__':
    settings = configparser.ConfigParser()
    settings.read(SETTINGS_FILE)
    
    #Authorize API calls
    helper.console_print('********Testing Twitter API********')
    [api, errors] = init_auth(settings['KEYS']['api_key'], settings['KEYS']['api_secret_key'])
    if api is None:
        helper.print_errors(errors)
        sys.exit(1)

    helper.console_print('********API authenticated. Testing features...********')

    # Get the profile of a user
    username = "BU_tweets"
    helper.console_print('********Get profile********')
    (userObj,errors) = getUserProfile(api, username)
    if userObj is None:
        helper.print_errors(errors)
        sys.exit(1)
    
    helper.console_print('name: ' + str(userObj.name))
    helper.console_print('screen_name: ' + str(userObj.screen_name))
    helper.console_print('description: ' + str(userObj.description))
    helper.console_print('url: ' + str(userObj.url))
    helper.console_print('followers_count: ' + str(userObj.followers_count))
    helper.console_print('created_at: ' + str(userObj.created_at))
    helper.console_print('statuses_count : ' + str(userObj.statuses_count))
    helper.console_print('')
    
    
    # Get the tweets of a user
    helper.console_print('********Get profile tweets********')
    (userTimelineList,errors) = getUserTimeline(api, username)
    
    if userTimelineList is None:
        helper.print_errors(errors)
        sys.exit(1)
    
    for tweet in userTimelineList:
        helper.console_print('created_at: ' + str(tweet.created_at))
        helper.console_print('text: ' + str(tweet.text ))
        helper.console_print('source: ' + str(tweet.source))
        helper.console_print('in_reply_to_user_id: ' + str(tweet.in_reply_to_user_id))
        helper.console_print('is_quote_status: ' + str(tweet.is_quote_status))
        helper.console_print('retweet_count: ' + str(tweet.retweet_count))
        helper.console_print('favorite_count: ' + str(tweet.favorite_count))
        helper.console_print('')

    # Find trending topic locations
    helper.console_print('********Getting trending locations...********')
    (locationsList, errors) = getTrendingLocations(api)
    if locationsList is None:
        helper.print_errors(errors)
        sys.exit(1)
    
    
    # Find trending topics in USA
    usa_woeid = 23424977
    helper.console_print('********Getting trending topics for USA...********')
    (trendingDict, errors) = getTrendingTopics(api, usa_woeid)
    if trendingDict is None:
        helper.print_errors(errors)
        sys.exit(1)

    helper.console_print('********Performing Twitter search...********')
    (list, errors) = doSearch(api, query='#BostonUniversity', count=100, result_type='popular')
    if list is None:
        helper.print_errors(errors)
        sys.exit(1)


    helper.console_print('********Test complete********')
    sys.exit(0)