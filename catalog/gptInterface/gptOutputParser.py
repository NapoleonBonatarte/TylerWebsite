import re
import json

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
        print(info['city'])


#cleanData({"Address":None, "sp_name":"hospice", "city": "Henderson", "state":"Nevada"})

# example call
#parselocationInfo("---BEGIN FORMAT TEMPLATE---\naddress: (null)\ndestination: (hospice)\ncity: (chicago)\n---END FORMAT TEMPLATE---")
