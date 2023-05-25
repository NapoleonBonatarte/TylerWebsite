import re
import json
import usaddress

#### NOTE: This is using a preloaded JSON file, change this in production

def giveInfo(info):
        file = open('catalog/gptInterface/sample.json')
        data = json.load(file)
        file.close()

        retInfo = dict({"name": info["name"]})

        print("GIVE INFO DATA", info)

        for i in data:
                if i["Name"].lower().replace(" ","") == info["name"].lower().replace(" ", ""):

                        print("THIS IS THE DATE BEING READ ",i)

                        if info["askAboutDataSet"] == True:
                                retInfo["Fax No"] = i["Fax No"]
                                retInfo["Email"] = i["Email"]
                                retInfo["Hours"] = i["WorkingHrs"]
                                retInfo["Insurance"] = i["Comm_Insurance_Accpt"]
                                retInfo["Medicaid_Accpt"] = i["Medicaid_Accpt"]
                                retInfo["Medicare_Accpt"] = i["Medicare_Accepted"]
                                retInfo["MMAI_plans"] = i["MMAI_plans"]
                                retInfo["SelfPay_Accept_Fees"] = i["SelfPay_accpt_Fees"]
                                retInfo["PCP referral"] = i["PCP referral/Pre-Auth required"]
                                retInfo["PT_type"] = i["Pt_type"]
                                retInfo["Lang_services"] = i["Lang_services"]
                                retInfo["Services"] = i["Services"]
                                retInfo["Transport_Assist"] = i["Transport Assist"]
                                retInfo["Notes"] = i["comments/notes"]
                                retInfo["Availability"] = i["Availability"]
                                retInfo["Pt_Portal"] = i["Pt_Portal"]
                                retInfo["website"] = i["Info_found"]
                                retInfo["Telehealth"] = i["Telehealth"]
                                retInfo["Specialty_Service"] = i["Specialty services/Other offerings"]

                        else:
                                if info["askAboutInsurance"] == True:
                                        retInfo["Insurance"] = i["Comm_Insurance_Accpt"]
                                if info["askAboutMedicare"] == True:
                                        retInfo["Medicare_Accpt"] = i["Medicare_Accepted"]
                                if info["askAboutMedicaid"] == True:
                                        retInfo["Medicaid_Accpt"] = i["Medicaid_Accpt"]
                                if info["askAboutWorkingHours"] == True:
                                        retInfo["Hours"] = i["WorkingHrs"]
                                if info["askAboutSelfPay"] == True:
                                        retInfo["SelfPay_Accept_Fees"] = i["SelfPay_accpt_Fees"]
                                if info["askAboutLanguageServices"] == True:
                                        retInfo["Lang_services"] = i["Lang_services"]

        return retInfo



def recommendLocation(info):
        # load file
        #### NOTE: change this setup to load json file from data base for quick integration
        #testPath = "catalog/gptInterface/"
        #print(os.listdir(testPath))

        file = open('catalog/gptInterface/sample.json')
        data = json.load(file)
        file.close()

        recomended_locations = []
        if (info["Address"] != None) and ((info["city"] is None) or (info["state"]is None)):
                info["city"] = findCityAndStateFromAddress(info)

        #### NOTE: lists seperated out based on fulfilled parameters, the
        # one directly below appends every location that fulfils the type of 
        # treatment response, such as fufilling every location that has cardiologists
        # this should allow for easier integration with a proper database

        #### NOTE: This is an inefficient way of doing things, and is only
        # being done due to lack of database access, please change this later


        ##### business name
        ## NOTE: this checks if a business name has been entered, if
        ## so it will only respond to questions about that business name


        



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

def parseInfo(loc):

        max_input = 150

        # fix this later
        loc = loc.replace("\n", "")

        addressString = ""
        destinationString = ""
        cityString = ""
        stateString = ""
        name = ""
        askAboutDataSet = False
        askAboutInsurance = False
        askAboutMedicare = False
        askAboutMedicaid = False
        askAboutWorkingHours = False
        askAboutSelfPay = askAboutLanguageServices = askAboutServices = False

        askAboutWorkingHours = checkIfStringinsideString("askworkinghourstrue", loc)
        askAboutSelfPay = checkIfStringinsideString("askselfpaytrue", loc)
        askAboutLanguageServices = checkIfStringinsideString("asklanguageservicetrue", loc)
        askAboutServices = checkIfStringinsideString("askaboutservicestrue", loc)
        if (re.search(r'\b(askdatatrue)\b',loc)):
                askAboutDataSet = True
        if (re.search(r'\b(askinsurancetrue)\b',loc)):
                askAboutInsurance = True
        if (re.search(r'\b(askmedicaretrue)\b',loc)):
                askAboutMedicare = True
        if (re.search(r'\b(askmedicaidtrue)\b',loc)):
                askAboutMedicaid = True

        nameIndex = re.search(r'\b(name)\b', loc).end()

        for i in range(nameIndex+3, nameIndex + (max_input + 3)):
                if loc[i] == ")":
                        break

                name += loc[i]

        addressStringIndex = re.search(r'\b(address)\b', loc).start()

        # address max characters is 150
        for i in range(addressStringIndex+10,addressStringIndex+(max_input+10)):

                if loc[i] == ")":
                        break

                addressString += loc[i]

        destinationStringIndex = re.search(r'\b(destination)\b', loc).start()

        for i in range(destinationStringIndex+14,destinationStringIndex+(max_input + 14)):

                if loc[i] == ")":
                        break

                destinationString += loc[i]

        cityStringIndex = re.search(r'\b(city)\b', loc).start()
        for i in range(cityStringIndex+7,cityStringIndex+(max_input+7)):

                if loc[i] == ")":
                        break

                cityString += loc[i]

        stateStringIndex = re.search(r'\b(state)\b', loc).start()

        for i in range(stateStringIndex+8,stateStringIndex+(max_input+8)):

                if loc[i] == ")":
                        break

                stateString += loc[i]

        return cleanData({"Address":addressString, "sp_name":destinationString, "city": cityString, "state":stateString, "askAboutDataSet": askAboutDataSet, "askAboutInsurance" : askAboutInsurance, "askAboutMedicare": askAboutMedicare, "askAboutMedicaid": askAboutMedicaid, "name": name,
                          "askAboutWorkingHours": askAboutWorkingHours, "askAboutSelfPay":askAboutSelfPay, "askAboutLanguageServices":askAboutLanguageServices, "askAboutMedicaid" :askAboutMedicaid,"askAboutMedicare":askAboutMedicare ,"askAboutServices": askAboutServices})

def checkIfStringinsideString(toCheck, loc):
        try:
                if re.search(rf"\b(?=\w){toCheck}\b(?!\w)", loc, re.IGNORECASE):
                        return True
        except:
                return False
        return False


def cleanData(info): # info should be a dict

        file = open("catalog/gptInterface/state.json")
        states = json.load(file)

        #print(states)

        if info['state'] != None:
                if len(info['state'])>2:
                        for i in states:
                                try:
                                        if i['name'].__str__().lower() == info["state"].lower():
                                                info['city'] = info['city'] + ", "+ i['abbreviation']
                                except:
                                        print("except1")
                else:
                        for i in states:
                                try:
                                        if i["abbreviation"].__str__().lower() == info["state"].lower():
                                                info['city'] = info['city'] + ", " + i["abbreviation"]
                                except:
                                        print("except2")
        #print(info)
        return info

def findCityAndStateFromAddress(info):
        address = usaddress.parse(info['Address'])
        city = ""
        state = ""
        for i in address:
                if i[1] == "PlaceName":
                        city += i[0]
                if i[1] == "StateName":
                        state += ", " + i[0]

#recommendLocation("---BEGIN FORMAT TEMPLATE---\naddress: (null)\ndestination: (Neurology)\ncity: (Henderson)\nstate: (Nevada)\n---END FORMAT TEMPLATE---")

