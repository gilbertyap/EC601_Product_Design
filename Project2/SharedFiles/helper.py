#---------------------------------------------
# File name: helper.py
# Description: Shares commonly used functions among project.
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: September 25, 2020
#---------------------------------------------

DEBUG_MODE=False

'''
Determines if statements should be made
Input: text:string
Output: None
'''
def console_print(text):
    if(DEBUG_MODE):
        print(text)

'''
Makes it easier to print text that is visible within the command line
Input: text:string
Output: None
'''
def print_with_stars(text):
    console_print('********' + text + '********')
    console_print('')

'''
Makes printing error lists easier
Input: errorList:list of string
Output: None
'''
def print_errors(errorList):
    console_print("Error! See the following errors(s): ")
    for statement in errorList:
        console_print(statement)
    console_print('')