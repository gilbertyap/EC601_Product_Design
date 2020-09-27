# Project 2 - Modularity and Third-Party APIs

## Requirements 
* **Windows 10** (May work on other operating systems, untested)
* **Python** (3.8.5 used)
* Twitter API Keys
* [Google Cloud SDK](https://www.google.com/search?client=firefox-b-1-d&q=google+cloud+sdk) and credentials authenticated on computer

## Installation:
* `git clone git@github.com:gilbertyap/EC601_Product_Design.git`
* `cd EC601_Product_Design/Project2`
* `pip install -r requirements.txt` - This will install all Python requirements.

## Summary
The goal of Project 2 is for students to get familiar with using third-party APIs and brainstorming user stories. There are a plethora of tools available to developers, but without a user story, these tools do not accomplish anything.

Project 2 is separated into two phases: Phase 1 and Phase 2.

Phase 1 was an opportunity for students to get famililar with using third-party APIs and open-source libraries. For the purpose of this phase, students were asked to explore the Twitter API and Google Cloud Natural Language Processing API. Using these two APIs, students had to demonstrate using these two tools to accomplish a goal. The demo that I completed consists of getting the top trending hashtag (out of twitters top 50 trends) with the most tweets in the last 24 hours and presenting the sentiment score of the top 50 (default, can be changed) search results of that hashtag. Then, the demo will go through the other top 50 trends and find other trending hashtags. Their sentiment scores will also be presented to give context to the sentiment score of the top hashtag.

## How to run

### Optional
There are built-in tests in `twitterCalls.py` and `nlpCalls.py`. Running either `python twitterCalls.py` or `python nlpCalls.py` will perform a test that calls every function within the file. This test is useful for ensuring that all functions used within `analyzeTwitter.py` are working properly.

### Phase 1
1. Users must first put their Twitter API into the settings.ini file. Users may also customize the `numSearchResults` between 1 and 200 to increase or decrease the number of tweets per hashtag exaimined for sentiment analysis.
2. Open an Admin command line console and run the demo with `python analyzeTwitter.py`.
3. Users should be presented with Google NLP sentiment scores for a number of hashtags via the command line. See `example.png` for example results.
