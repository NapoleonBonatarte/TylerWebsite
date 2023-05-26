import openai


newMessagesToAdd = []

def parseUserInfo(patientRequest, newGPTMessage):
        global newMessagesToAdd
        print("beggining user parse")

        addingMessage = []

        for i in newGPTMessage:
                addingMessage.append(i["name"])


        if newGPTMessage != None and newGPTMessage != []:
                GPTMessages = newGPTMessage

        GPTMessages = [{"role": "system","content":"""you are parsing a sentance. please do not analyze the user sentance, only parse it
                        use the template below to parse the given information. For anything in the template that starts with
                        (askAbout) answer in the form of either (True) or (False). Do not answer user questions. if you can match the name to a name in the given data set do so.
                        input destination in the folowing way: (Dental Care, Neurology, Cardiology, Internal Medicine, Allergy, Dermatology, COVID Testing Places, Dialysis Clinics
                        Endocrinology, Pain Management, Pharmacy, Donation Closets, Food Pantries, Home Health, Mental health, Primary Care
                        Pulmonology, Rheumatology, Urology, Radiology, Plastic Surgery, Hematology Oncology, Virtual Care, Housing, Transportation).
                        ---BEGIN FORMAT TEMPLATE---
                        name: (${name})
                        address: (${address})
                        destination: (${destination_type})
                        city: (${city})
                        state: (${state})
                        askAboutDataSet: (askdata${askAboutDataSet})
                        askAboutInsurance: (askinsurance${askAboutInsurance})
                        askAboutMedicare: (askmedicare${askAboutMedicare})
                        askAboutMedicaid: (askmedicaid${askAboutMedicaid})
                        askAboutWorkingHours: (askworkinghours${askAboutWorkingHours})
                        askAboutSelfPay: (askselfpay${askAboutSelfPay})
                        askAboutLanguageServices: (asklangservice${askAboutLanguageServices})
                        askAboutServices: (askaboutservice${askAboutServices})
                        insurance: (${insurance})
                        acceptMedicare: (${acceptMedicare})
                        acceptMedicaid: (${acceptMedicaid})


                        ---END FORMAT TEMPLATE---"""},
                        {"role": "user", "content": """I am going to ask you a question, I do not want you to answer my question, I only want you to parse the question, 
                        so if I ask (can you find cardiology centers in chicago that have spanish speakers and accept aetna insurance and have medicare?) you should output 
                        name: (null)
                        address: (null)
                        destination: (cardiology)
                        city: (chicago)
                        state: (null)
                        askAboutDataSet: (askdatafalse)
                        askAboutInsurance: (askinsurancefalse)
                        askAboutMedicare: (askmedicarefalse)
                        askAboutMedicaid: (askmedicaidfalse)
                        askAboutWorkingHours: (askworkinghoursfalse)
                        askAboutSelfPay: (askselfpayfalse)
                        askAboutLanguageServices: (asklangservicetrue)
                        askAboutServices: (askaboutservicefalse)
                        insurance: (aetna)
                        acceptMedicare: (yes)
                        acceptMedicaid: (no)
                        
                        another example would be: (can you tell me more about the Dental Care of St.Rose?) your name output
                        would be (name: (Dental Care of St.Rose) askAboutDataSet: (askdatatrue)), if the user says (tell me more
                        about {name} you should say output (askdatatrue) in the fromat given by the administrator"""},
                        {"role" : "user", "content": patientRequest}]
        
        GPTMessages += addingMessage

        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= GPTMessages,
                temperature=0.1,
                n=1
        )


        print(completion)
        result=completion.choices[0].message.content
        #a = recommendLocation(result)

        #print(a, "THIS IS THE DATASET")

        #newMessagesToAdd.append({"role":"assistant", "content": """Please use this data to answer any questions
        #that the user asks you. %s""" %a[:4]})

        #print(GPTMessages)

        #print(result)
        """""
        if len(a) < 1:
                print("RETURNING NONE")
                return None, False
                """
        return result, False
