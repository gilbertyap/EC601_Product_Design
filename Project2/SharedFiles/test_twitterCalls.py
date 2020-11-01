#---------------------------------------------
# File name: test_twitterCalls.py
# Description: pytest file for twitterCalls
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: October 29, 2020
#---------------------------------------------

import helper, twitterCalls
import pytest, os, sys

def test_twittercalls():
    #Authorize API calls
    (api, errors) = twitterCalls.init_auth(os.getenv('API_KEY'), os.getenv('API_SECRET_KEY'))
    assert(api is not None)
    if api is None:
        helper.print_errors(errors)
        

    return (api, errors)

def test_getProfile():
    api, errors = test_twittercalls()

    # Get the profile of a user
    username = "BU_tweets"
    helper.print_with_stars('Get profile')
    (userObj,errors) = twitterCalls.getUserProfile(api, username)
    assert (userObj is not None)
    if userObj is None:
        helper.print_errors(errors)
        

    helper.console_print('name: ' + str(userObj.name))
    helper.console_print('screen_name: ' + str(userObj.screen_name))
    helper.console_print('url: ' + str(userObj.url))
    helper.console_print('')

    assert 'Boston University' in str(userObj.name)
    assert 'BU_Tweets' in str(userObj.screen_name)
    assert 'http://t.co/L9mQIxl5yQ' in str(userObj.url)

def test_getTweet():
    api, errors = test_twittercalls()
    
    # Get a particular tweet and check its text
    helper.print_with_stars('Get particular tweet')
    (tweetObj, errors) = twitterCalls.getTweet(api, 1270748783387840520)
    assert (tweetObj is not None)
    if tweetObj is None:
        helper.print_errors(errors)
        

    helper.console_print('Tweet ID: 1270748783387840520')
    helper.console_print('Text: ' + str(tweetObj.full_text))
    compareText = 'Have questions regarding BU’s return to class, the lab, and life on campus this fall? Our Back2BU website has the answers guided by public health considerations and best practices.'
    assert compareText in tweetObj.full_text

def test_getUserTimeline():
    api, errors = test_twittercalls()
    
    username = "BU_tweets"
    (tweetObjList,errors) = twitterCalls.getUserTimeline(api, username)
    assert (tweetObjList is not None)
    if tweetObjList is None:
        helper.print_errors(errors)
        

def test_getTrendingLocations():
    api, errors = test_twittercalls()
    
    # Find trending topic locations
    helper.print_with_stars('Getting trending locations...')
    (locationsList, errors) = twitterCalls.getTrendingLocations(api)
    assert (locationsList is not None)
    if locationsList is None:
        helper.print_errors(errors)
        

def test_getTrendingTopics():
    api, errors = test_twittercalls()
    
    # Find trending topics in USA
    usa_woeid = 23424977
    helper.print_with_stars('Getting trending topics for USA...')
    (trendingDict, errors) = twitterCalls.getTrendingTopics(api, usa_woeid)
    assert (trendingDict is not None)
    if trendingDict is None:
        helper.print_errors(errors)
        

    helper.console_print('Trends found')

def test_doSearch():
    api, errors = test_twittercalls()

    helper.console_print('Performing Twitter search...')
    (tweetList, errors) = twitterCalls.doSearch(api, query='#BostonUniversity', count=10, result_type='top')
    assert (tweetList is not None)
    if tweetList is None:
        helper.print_errors(errors)
        
    helper.console_print('Tweets with #BostonUniversity found')

if __name__ == '__main__':
    helper.console_print('Testing Twitter API features')
    test_twittercalls()
    test_getProfile()
    test_getTweet()
    test_getUserTimeline()
    test_getTrendingLocations()
    test_getTrendingTopics()
    test_doSearch()
    helper.console_print('Test complete')
    sys.exit(0)