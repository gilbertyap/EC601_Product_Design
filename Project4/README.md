# Project 4 - Unit Testing and Code Review

## Requirements

* Python 3.6 or greater

## Installation
* `git clone git@github.com:gilbertyap/EC601_Product_Design.git`
* `cd /Project2/`
* `pip install -r requirements.txt`

## Summary

### Phase 1

The goal of Project 4 Phase 1 was become familiar with GitHub Actions and unit tests (for Python using `pytest`). GitHub Actions and unit tests are useful tools for making sure that code remains functional and as bug-free as possible throughout the development process. These tools help companies and groups stick to a "Continuous Integration" and "Continuous Deployment" or "Continuous Delivery" methodology set. These practices help developers and users alike.

'Continuous Integration" (CI) is the practice of having developers regularly contribute to the same code base. CI helps make detecting errors and bugs easier since each change is logged and attributed to a time and/or a developer. Git is a popular example of a CI system, where deployed code can be kept in one branch while features being developed can be kept in separate or local branches. When the feature is finished, it can be put pushed to a separate remote branch for testing. GitHub actions can be used to run sytanx checks or alternate environment checks without additional setup in your own workspace.

"Continuous Deployment" and "Continuous Delivery" both refer to the practice of having the software product deployable at any time. If Git is being used, this means having a branch that is always kept functional while developing and testing new features. Both methods allow companies or groups deploy fixes or updates without having to follow a rigid schedule. While both "Continuous Delivery" and "Continuous Deployment" utilize automated unit tests and integration, "Continuous Delivery" keeps the final production deployment a manual process unlike "Continous Deployment". 

During Project 2, I had developed a rudimentary unit test within `twitterCalls.py` and `nlpCalls.py`. When calling these wrapper files, it would run through a short test of the helper functions that made it easier for me to test each new helper function that I added. However, this meant that it was my responsiblity to run each of these files when I made updates. There would be times that I added new functions without adding them to the test bench, which would lead to bugs being pushed to my master branch. During Phase 1 of Project 4, I moved these test benches to new files called `test_twitterCalls.py` and `test_nlpCalls.py` so that I could run the tests with `pytest`. With `pytest`, I was able to easily automate these tests, allowing me to see all errors for individual functions that could be tested in parallel. However, since a majority of my code for Project 2 was either based on GUI input or API calls, I am unable to `pytest` to my GitHub actions. It would be impossible to write unit tests to test every possible GUI element and input combination, so if I were to continue working on Project2's code I would need to continue testing the GUI manually. Fortunately, I had  experience using `PyQt` at my previous job where we had designed a new software product that had an even greater number of user input possibilities.

After finding out about GitHub Secrets from our class Slack channel, I attempted to set up `pytest` in my workflow. As of November 1st, there seems to be an issue with installing `matplotlib` through GitHub actions on both their Ubuntu and Windows virtual environments. The issue seems to stem from the installation of `kiwisolver`, which is part of `matplotlib`'s dependencies. I have kept the `master` branch as it was prior to utilizing `pytest` in GitHub Actions. The branch `project4` can be viewed to see the updated `main.yml` file that is used for the GitHub Actions workflow with `pytest`.

## How to Run

### Phase 1

Pushing a commit to the `project4` branch will trigger the GitHub action that runs `flake8`. To test the API wrapper libraries, users should clone this repository and add their API key and API secret key to the `/Project2/SharedResources/settings.ini` file and run `pytest`. 

## Issues

### Phase 1
* ~~Since it would not be advisable to push API keys to the GitHub repository, I have to run `pytest` on my folder offline. Additionally, ~~ Since Project 2 mainly relies on user input in the GUI, I am unable to add unit tests for that. I instead focused on offline API wrapper testing.

* After checking the logs of the GitHub Actions, I saw that my code received many warnings and "errors" from flake8, but all of them were mainly stylistic formatting issues. I have chosen to ignore them at this time.

* When I first set up the GitHub action `Project 2 Testing`, I knew I wanted to test multiple version of Python and multiple OS's. In the beginning, I ran into trouble setting up the YAML file because I did not differentiate the command line arguements for Ubuntu and Windows. I also had some issues figuring out the pathing in the GitHub virtual machines, but I eventually figured out that I should use relative pathing to install the `requirements.txt` files in Project2 directory.

* I had also thought about adding a Python version 2.7 test to my unit test. Although the libraries that I used for Project 2 should work with Python 2.7, I realized that I had wrote most of my print functionality in the Python 3 way. I knew for sure that my code would return many errors if I tested against Python 2.7, so in this repo I should specifically state that Python 3+ is required.

* There is an issue in the installation of `matplotlib` through GitHub Actions that is preventing my workflow from running the `flake8` tests or `pytest`. [It can be seen here](https://github.com/gilbertyap/EC601_Product_Design/actions) that 4 of the last 11 automated tests passed, and none have passed since October 29th due to the mentioned issue.