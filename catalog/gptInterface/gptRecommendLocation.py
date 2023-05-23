import re
import json

#### NOTE: This is using a preloaded JSON file, change this in production

def recommendLocation(info):
        # load file
        #### NOTE: change this setup to load json file from data base for quick integration
        file = open('TylerWebsite\catalog\gptInterface\sample.json')
        data = json.load(file)
        # dictionary
        info = parselocationInfo(info)

        recomended_locations = []


        #### NOTE: lists seperated out based on fulfilled parameters, the
        # one directly below appends every location that fulfils the type of 
        # treatment response, such as fufilling every location that has cardiologists
        # this should allow for easier integration with a proper database

        #### NOTE: This is an inefficient way of doing things, and is only
        # being done due to lack of database access, please change this later

        # sp_name
        sp_nameCandidates = []

        for i in data:
                if i["sp_name"].lower() == info["sp_name"].lower():
                        sp_nameCandidates.append(i)
        
        #print(sp_nameCandidates)

        # city
        cityCandidates = []

        for i in data:
                if i["record_id"].lower() == info["city"].lower():
                        cityCandidates.append(i)

        #print(cityCandidates)
        # address
        # NOTE: add this later

        finalCandidateList = []

        for i in sp_nameCandidates:
                if i in cityCandidates:
                        finalCandidateList.append(i)

        #print(finalCandidateList)
        
        return finalCandidateList



#################################################################
#### NOTE: this is the same code as in gptOutputParser.py
#### NOTE: it is here because relative imports do not want to work
#### NOTE: with django for some reason
#################################################################

def parselocationInfo(loc):

        max_input = 150

        # fix this later
        loc = loc.replace("\n", "")

        addressString = ""
        destinationString = ""
        cityString = ""
        stateString = ""

        addressStringIndex = re.search(r'\b(address)\b', loc).start()
        #addressStringIndex = addressStringIndex.start()
        #print(addressStringIndex.start(), "THIS IS THE LOCATION OF address")

        # address max characters is 150
        for i in range(addressStringIndex+10,addressStringIndex+(max_input+10)):

                if loc[i] == ")":
                        break

                addressString += loc[i]

        #print(addressString)


        destinationStringIndex = re.search(r'\b(destination)\b', loc).start()
        #print(destinationStringIndex.start(), "THIS IS THE LOCATION OF destination")

        for i in range(destinationStringIndex+14,destinationStringIndex+(max_input + 14)):

                if loc[i] == ")":
                        break

                destinationString += loc[i]

        #print(destinationString)

        cityStringIndex = re.search(r'\b(city)\b', loc).start()
        #print(cityStringIndex.start(), "THIS IS THE LOCATION OF CITY")
        for i in range(cityStringIndex+7,cityStringIndex+(max_input+7)):

                if loc[i] == ")":
                        break

                cityString += loc[i]

        #print(cityString)

        stateStringIndex = re.search(r'\b(state)\b', loc).start()

        for i in range(stateStringIndex+8,stateStringIndex+(max_input+8)):

                if loc[i] == ")":
                        break

                stateString += loc[i]

        return cleanData({"Address":addressString, "sp_name":destinationString, "city": cityString, "state":stateString})


def cleanData(info): # info should be a dict

        file = open("TylerWebsite\catalog\gptInterface\state.json")
        states = json.load(file)

        if info['state'] != None:
                if len(info['state'])>2:
                        for i in states:
                                try:
                                        if i['name'].__str__() == info["state"]:
                                                info['city'] = info['city'] + ", "+ i['abbreviation']
                                except:
                                        print("except1")
                else:
                        for i in states:
                                try:
                                        if i["abbreviation"].__str__() == info["state"]:
                                                info['city'] = info['city'] + ", " + i["abbreviation"]
                                except:
                                        print("except2")
        return info

recommendLocation("---BEGIN FORMAT TEMPLATE---\naddress: (null)\ndestination: (Neurology)\ncity: (Henderson)\nstate: (Nevada)\n---END FORMAT TEMPLATE---")

