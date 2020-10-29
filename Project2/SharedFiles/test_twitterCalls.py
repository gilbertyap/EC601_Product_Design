#---------------------------------------------
# File name: test_twitterCalls.py
# Description: pytest file for twitterCalls
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: October 29, 2020
#---------------------------------------------

import configparser, helper, twitterCalls
import pytest, sys



def test_twittercalls():
    SETTINGS_FILE = 'settings.ini'
    settings = configparser.ConfigParser()
    settings.read(SETTINGS_FILE)
    
    #Authorize API calls
    helper.console_print('Testing Twitter API')
    [api, errors] = twitterCalls.init_auth(settings['KEYS']['api_key'], settings['KEYS']['api_secret_key'])
    if api is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    helper.console_print('API authenticated. Testing features...')

    # Get the profile of a user
    username = "BU_tweets"
    helper.print_with_stars('Get profile')
    (userObj,errors) = twitterCalls.getUserProfile(api, username)
    if userObj is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    helper.console_print('name: ' + str(userObj.name))
    helper.console_print('screen_name: ' + str(userObj.screen_name))
    helper.console_print('url: ' + str(userObj.url))
    helper.console_print('')

    assert 'Boston University' in str(userObj.name)
    assert 'BU_Tweets' in str(userObj.screen_name)
    assert 'http://t.co/L9mQIxl5yQ' in str(userObj.url)

    # Get a particular tweet and check its text
    helper.print_with_stars('Get particular tweet')
    (tweetObj, errors) = twitterCalls.getTweet(api, 1270748783387840520)
    
    if tweetObj is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    helper.console_print('Tweet ID: 1270748783387840520')
    helper.console_print('Text: ' + str(tweetObj.full_text))
    compareText = 'Have questions regarding BU’s return to class, the lab, and life on campus this fall? Our Back2BU website has the answers guided by public health considerations and best practices.'
    assert compareText in tweetObj.full_text

    (tweetObjList,errors) = twitterCalls.getUserTimeline(api, username)
    if tweetObjList is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    # Find trending topic locations
    helper.print_with_stars('Getting trending locations...')
    (locationsList, errors) = twitterCalls.getTrendingLocations(api)
    if locationsList is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)
    
    # Find trending topics in USA
    usa_woeid = 23424977
    helper.print_with_stars('Getting trending topics for USA...')
    (trendingDict, errors) = twitterCalls.getTrendingTopics(api, usa_woeid)
    if trendingDict is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    helper.console_print('Trends found')

    helper.console_print('Performing Twitter search...')
    (list, errors) = twitterCalls.doSearch(api, query='#BostonUniversity', count=10, result_type='top')
    if list is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)

    helper.console_print('Tweets with #BostonUniversity found')

    helper.console_print('Test complete')

if __name__ == '__main__':
    test_twittercalls()
    sys.exit(0)