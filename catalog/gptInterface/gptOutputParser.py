"""
Author: Tyler Windemuth
Updated: 5/29/23

This file parses various inputs from the User and from GPT into outputs
"""



import re
import json
import usaddress

#### NOTE: This is using a preloaded JSON file, change this in production

def giveInfo(info):
        file = open('catalog/gptInterface/sample.json')
        data = json.load(file)
        file.close()

        retInfo = dict({"name": info["name"]})

        #print("GIVE INFO DATA", info)

        for i in data:
                if i["Name"].lower().replace(" ","") == info["name"].lower().replace(" ", ""):

                        if info["askAboutDataSet"] == True:
                                # This is disgusting, rework this later
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
                                # same above as below
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
                                if info['askAboutInsurance'] == True:
                                        retInfo['Insurance'] = i['Comm_Insurance_Accpt']
                                if info['doesAcceptInsurance'] == True:
                                        acceptedInsurances = i['Comm_Insurance_Accpt']

                                        acceptedInsurancesList = acceptedInsurances.strip().split(",")
                                        print(acceptedInsurancesList, " THIS IS A LIST OF THE ACCEPTED INSURANCES")

                                        if info["insuranceToCheck"] in acceptedInsurancesList:
                                                retInfo += str(info["insuranceToCheck"]) + " is accepted by %s" %info['name']  

        
        print(retInfo, "RETINFO")

        return retInfo



def recommendLocation(info):
        # load file
        #### NOTE: change this setup to load json file from data base for quick integration
        #testPath = "catalog/gptInterface/"
        #print(os.listdir(testPath))

        #print("RECOMENDING LOCATION")
        #print("INFO BEING USED TO RECOMMEND: ",info)

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

        # sp_name
        sp_nameCandidates = []

        #print(info, " INFORMATION BEING PASSED TO RECOMEND LOCATION")

        for i in data:
                for j in info["sp_name"]:
                        #print("--------------------------")
                        #print(j.lower(), " SPECIALITY BEING CHECKED")
                        #print(i["sp_name"].lower(), " SPECIALITY BEING CHECKED AGAINST")
                        if j.lower().strip() == i['sp_name'].lower():
                                #print(i["Name"], " CANDIDATE ACCEPTED")
                                sp_nameCandidates.append(i)

        #print('THESE ARE THE CANDIDATES----sp_name----------')

        #print('END OF CANDIDATES--------------')
                
        
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


        print("FINAL CANDIDATE LIST: ", finalCandidateList)

        retList = []
        insurancesAccepted = []
        if info['insuranceToCheck'] != "null":
                #print("IF 1")
                #print("BUSINESS NAMES--------------")
                for business in finalCandidateList:
                        #print("FINDING INSURANCE")
                        #print(business['Comm_Insurance_Accpt'], "-----------------")

                        if business['Comm_Insurance_Accpt'] != None:
                                insurancesAccepted = business['Comm_Insurance_Accpt'].strip().lower().split(";")
                                for i in range(len(insurancesAccepted)):
                                        #print(insurancesAccepted[i], " Specific_insurance")
                                        insurancesAccepted[i] = insurancesAccepted[i].strip()
                                #print(insurancesAccepted, " INSURANCES ACCEPTED AT: " + business['Name'])
                                if info['insuranceToCheck'].lower().strip() in insurancesAccepted:
                                        #print("ACCEPTED")
                                        retList.append(business)
        else:
                retList = finalCandidateList
        
        return retList



#################################################################
#### NOTE: this is the same code as in gptOutputParser.py
#### NOTE: it is here because relative imports do not want to work
#### NOTE: with django for some reason
#################################################################

def parseInfo(loc):

        print("PARSEINFO")

        max_input = 150

        # fix this later
        #print(type(loc))
        #print(loc, "THIS IS THE INFO PASSED TO PARSE INFO")
        try:
                loc = loc.replace("\n", "")
        except:
                pass

        addressString = ""
        destinationString = ""
        cityString = ""
        stateString = ""
        name = ""
        doesAcceptInsurance = False
        insuranceToCheck = ""
        destinations = []
        askAboutDataSet = False
        askAboutInsurance = False
        askAboutMedicare = False
        askAboutMedicaid = False
        askAboutWorkingHours = False
        askAboutSelfPay = askAboutLanguageServices = askAboutServices = False




        insuranceIndex = 0

        insuranceSearch = re.search(r'\b(dai:False)\b',loc)
        if insuranceSearch == None:
                print("RUNNING INSURANCE CHECL")
                try:    
                        insuranceIndex = re.search(r'\b(insurance)\b',loc).end()
                        print(insuranceIndex, ": INSURANCE INDEX")
                        for i in range(insuranceIndex+3,insuranceIndex+150):
                                if loc[i] == ")":
                                        break

                                insuranceToCheck += loc[i]

                except Exception as e:
                        print(e)
                        pass
        else:
                try:
                        insuranceSearchIndex = insuranceSearch.end()
                        if not insuranceSearch:
                                doesAcceptInsurance = True
                                for i in range(insuranceSearchIndex+4,insuranceSearchIndex+150):
                                        if loc[i] == ")":
                                                break

                                        insuranceToCheck += loc[i]
                except:
                        pass
                

        askAboutWorkingHours = checkIfStringinsideString("awh:True", loc)
        askAboutSelfPay = checkIfStringinsideString("asp:True", loc)
        askAboutLanguageServices = checkIfStringinsideString("als:True", loc)
        askAboutServices = checkIfStringinsideString("aas:True", loc)
        if (re.search(r'\b(aae:True)\b',loc)):
                askAboutDataSet = True
        if (re.search(r'\b(in:True)\b',loc)):
                askAboutInsurance = True
        if (re.search(r'\b(amr:True)\b',loc)):
                askAboutMedicare = True
        if (re.search(r'\b(amd:True)\b',loc)):
                askAboutMedicaid = True

        try:
                nameIndex = re.search(r'\b(name)\b', loc).end()
        except:
                return loc, False

        for i in range(nameIndex+3, nameIndex + (max_input + 3)):
                if loc[i] == ")":
                        break

                name += loc[i]

        try:
                addressStringIndex = re.search(r'\b(address)\b', loc).start()

                # address max characters is 150
                for i in range(addressStringIndex+10,addressStringIndex+(max_input+10)):

                        if loc[i] == ")":
                                break

                        addressString += loc[i]
        except:
                pass


        try:
                destinationStringIndex = re.search(r'\b(destination)\b', loc).start()

                for i in range(destinationStringIndex+14,destinationStringIndex+(max_input + 14)):

                        if loc[i] == ")":
                                break

                        destinationString += loc[i]
                
                destinations = destinationString.split(",")
                #print(destinations, " THESE ARE THE DESINATIONS BEING PASSED")
        except:
                pass

        try:

                cityStringIndex = re.search(r'\b(city)\b', loc).start()
                for i in range(cityStringIndex+7,cityStringIndex+(max_input+7)):

                        if loc[i] == ")":
                                break

                        cityString += loc[i]
        except:
                pass

        try:

                stateStringIndex = re.search(r'\b(state)\b', loc).start()

                for i in range(stateStringIndex+8,stateStringIndex+(max_input+8)):

                        if loc[i] == ")":
                                break

                        stateString += loc[i]
        except:
                pass

        print("INSURANCE TO CHECK: " +insuranceToCheck)

        return cleanData({"Address":addressString, "sp_name":destinations, "city": cityString, "state":stateString, "askAboutDataSet": askAboutDataSet, "askAboutInsurance" : askAboutInsurance,
                           "askAboutMedicare": askAboutMedicare, "askAboutMedicaid": askAboutMedicaid, "name": name,
                          "askAboutWorkingHours": askAboutWorkingHours, "askAboutSelfPay":askAboutSelfPay, "askAboutLanguageServices":askAboutLanguageServices, 
                          "askAboutMedicaid" :askAboutMedicaid,"askAboutMedicare":askAboutMedicare ,"askAboutServices": askAboutServices, "doesAcceptInsurance": doesAcceptInsurance, "insuranceToCheck":insuranceToCheck}), True

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

