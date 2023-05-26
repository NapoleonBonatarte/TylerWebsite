import re
import json
import os

def findNameInData(userInput):
        file = open("TylerWebsite/catalog/gptInterface/sample.json")
        dataList = json.load(file)
        file.close()

        #print(dataList)

        cleanedUserInput = userInput.lower().strip().split(" ")

        print(cleanedUserInput)

        for data in dataList:

                businessNames = data['Name'].lower().strip().split(" ")
                max_correct_inputs = len(businessNames)
                correct_inputs = 0
                #print(businessNames)

                for inputpoint in cleanedUserInput:
                        if inputpoint in businessNames:
                                correct_inputs += 1
                if (correct_inputs // max_correct_inputs) >= 0.75:
                        print("NAME FOUND", data['Name'])


findNameInData("I need to find what insurance rainbow dental care accepts")