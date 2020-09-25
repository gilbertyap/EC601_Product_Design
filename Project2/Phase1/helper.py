#---------------------------------------------
# File name: helper.py
# Description: Shares commonly used functions among project.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

def print_with_stars(text):
    print('********' + text + '********')
    print()


def print_errors(errorList):
    print("Error! See the following errors(s): ")
    for statement in errorList:
        print(statement)
    print()