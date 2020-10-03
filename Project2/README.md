# Project 2 - Modularity and Third-Party APIs

## Requirements
* **Windows 10** (May work on other operating systems, untested)
* **Python** (3.8.5 used), libraries can be installed as outlined below.
* Twitter API Keys
* [Google Cloud SDK](https://www.google.com/search?client=firefox-b-1-d&q=google+cloud+sdk) and credentials authenticated on computer

## Installation
* `git clone git@github.com:gilbertyap/EC601_Product_Design.git`
* `cd EC601_Product_Design/Project2`
* `pip install -r requirements.txt` - This will install all Python requirements.
* For Phase 1: `cd Phase1`, `python analyzeTwitter.py`
* For Phase 2: `cd Phase2`, `python phase2app.py`

## Summary
The goal of Project 2 is for students to get familiar with using third-party APIs and brainstorming user stories. There are a plethora of tools available to developers, but without a user story, these tools do not accomplish anything.

Project 2 is separated into two phases: Phase 1 and Phase 2.

Phase 1 was an opportunity for students to get famililar with using third-party APIs and open-source libraries. For the purpose of this phase, students were asked to explore the Twitter API and Google Cloud Natural Language Processing API. Using these two APIs, students had to demonstrate using these two tools to accomplish a goal. The demo that I completed consists of getting the top trending hashtag (out of twitters top 50 trends) with the most tweets in the last 24 hours and presenting the sentiment score of the top 50 (default, can be changed) search results of that hashtag. Then, the demo will go through the other top 50 trends and find other trending hashtags. Their sentiment scores will also be presented to give context to the sentiment score of the top hashtag.

Phase 2 was designed to have students design a MVP for an intended user story. For this project, I considered the following user stories:

```1. I am a therapist. I want to track the mood of my patients by processing their Twitter feed. Being able to see this information visually would be helpeful, as I am not familiar with programming.```

I first asked myself how tweet analysis could be used. For non-corporation Twitter accounts, tweets are often very personal and reflections of the user's mood. This type of information could be very useful to healthcare professionals such as therapists. Therapists can have a range of technical skills, so it would be easier to provide this software in a GUI.

```2. I am a data scientist. I am interested in tracking the sentiment score of multiple users over a specific period of time. I am interested in comparing each user's data and seeing if there are similarities over certain periods of time. I would like to compile each user's data in a standard file such as a .csv.```

From a data scientist's perspective, they would want to be able to fetch and locally save data. This prompted me to add the "export" features of my GUI. The .csv format is standard and is easily opened/used in other software.

```3. I am an ordinary user. I am interested in seeing emotion score over time for a user. I just want to see the information visually in a simple application. I do not want to fuss with command line arguements or interacting with a command line interface because it is intimidating.```

I also felt that this tool should be easy to use for an ordinary computer user. This means that the UI should be clean and intuitive. The user is able to type in most of the information in the GUI, which makes it much easier than relying on button clicks. 

In the case of my Phase 2 project, I expanded on my Phase 1 code and created a Python program that will process the sentiment score of a Twitter user's timeline over a time period. I wanted to present the information in a simple UI along with some visual information. I used `PySide2` and `PyQt5` to make the GUI for Phase 2.

## How to run

### Optional
There are built-in tests in `twitterCalls.py` and `nlpCalls.py`. Running either `python twitterCalls.py` or `python nlpCalls.py` will perform a test that calls every function within the file. This test is useful for ensuring that all functions used within `analyzeTwitter.py` are working properly.

### Phase 1
1. Users must first put their Twitter API into the settings.ini file. ~~Users may also customize the `numSearchResults` between 1 and 200 to increase or decrease the number of tweets per hashtag exaimined for sentiment analysis.~~ This parameter was removed in Phase 2.
2. Open an Admin command line console and run the demo with `python analyzeTwitter.py`.
3. Users should be presented with Google NLP sentiment scores for a number of hashtags via the command line. See `example.png` for example results.

### Phase 2
1. Same as step 1 of Phase 1.
2. Open an Admin command line console and run the demo with `python phase2app.py`.
3. The GUI that loads is split into two parts: the left is user input and the right is a `matplotlib` figure (similar to Matlab's plot window). On the left, the user can input username and start/end dates. Once the user has input all of these parameters, they can press "Get Sentiment" to process the user's tweets from that time period. This can take a few minutes, but once finished, the plot will appear on the right.
4. Once the user has generated a plot, the button labeled "Export data as csv files" becomes available. Pressing this buttong generates 2 .csv files named "$date$_$username$_score.csv" and "$date$_$username$_magnitude.csv" ($date$ and $username$ are generated).

### Issues
* One issue that came up in Phase 2 was the rate limit error. Since it is possible to fetch tweets from a large period of time, it is easy to hit the 1500 tweets/15-min and 100,000 tweets per 24-hours if you run many tests in a row. In this case, it is important to warn the user of the errors that have occured and give suggestions. I have a built-in error pop up system for this very reason.