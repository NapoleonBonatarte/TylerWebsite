"""
Author: Tyler Windemuth
Updated: 5/27/23

This file contains search function for user input, mainly used to
find certain values that are then used to skip portions of GPT response
"""



import json
import time
from difflib import SequenceMatcher

def findNameInData(userInput):
        file = open("catalog/gptInterface/sample.json")
        dataList = json.load(file)
        file.close()

        #print(dataList)

        cleanedUserInput = userInput.lower().strip().split(" ")

        print(cleanedUserInput)
        time1 = time.time()
        for data in dataList:

                businessNames = data['Name'].lower().strip().split(" ")
                max_correct_inputs = len(businessNames)
                correct_inputs = 0
                #print(businessNames)


                # NOTE: maybe use levenshetein distances here to allow for more user error while still getting an appropriate output.
                #       currently this is very slow
                for inputpoint in cleanedUserInput:
                        inputpoint.lower()
                        if (inputpoint in businessNames):
                                correct_inputs += 1
                        else:
                                for word in businessNames:
                                        #print(inputpoint,word.lower())
                                        #print(SequenceMatcher(None, inputpoint,word.lower()).ratio())
                                        if SequenceMatcher(None, inputpoint.lower(),word.lower()).ratio() > .75:
                                                correct_inputs += 1



                if (correct_inputs // max_correct_inputs) >= 0.75:
                        time2 = time.time()
                        print("RETTRUE")
                        print("TIME TAKEN TO RUN WORD SEACH: ", time2-time1)
                        return True, data
        print("RETFALSE")
        time2 = time.time()
        print("TIME TAKEN TO RUN WORD SEACH: ", time2-time1)
        return False, data


#findNameInData("I need to find what insurance rainbow dental care accepts")