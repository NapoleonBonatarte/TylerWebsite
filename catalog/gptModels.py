import openai

def parseUserInfo(patientRequest):
        
        completion = openai.ChatCompletion.create(
                 model="gpt-3.5-turbo",
                 messages=[{"role": "system","content":"""you are making a list of information about a patient, you are to parse their current address, and then you
                        will figure out thier destination type, this destination type will include, but are not limited to cardiology, hospice, allergy, COVID testing places, Dental Care, dermatology, dialysis Clinics, donation Closets, ED MAT, Endocrinology, ENT, Food Pantries, Free Clinics, General Surgery, GI, Hematology oncology, home health, infectious Disease, internal Medicine
                        and food pantry. then output them in the following format, please use this format without adding any words before or after the format,
                        sometimes the user will state the city they want instead of the address, if this happens set the address to null and fill in the city field in the formatted output, if any information is not included place null in the formatted output, 
                        do not ask the user any questions. if there are multiple destination types put them in a comma delineated format.
                        do not try to figure out if the city exists, or where it is. please do not analyze the user sentance, only parse it
                        ---BEGIN FORMAT TEMPLATE---
                        address: (${address})
                        destination: (${destination_type})
                        city: (${city})
                        ---END FORMAT TEMPLATE---"""},
                        {"role": "user", "content": """I am going to ask you a question, I do not want you to analyze it, I only want you to parse the question, 
                        so if I ask (can you find cardiology centers in chicago) you should output 
                        ---BEGIN FORMAT TEMPLATE---
                        address: (null)
                        destination: (cardiology)
                        city: (chicago)"""},
                        {"role" : "user", "content": patientRequest}],
                temperature=0.1,
                n=1
        )

        print(completion)
        result=completion.choices[0].message.content
        return result