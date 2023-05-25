

def buildLocationOutput(info, listIndex):
        print("LIST INDEX", listIndex)
        if info == None:
                return "<p> No matches were found </p>"
        
        # Change this to not be hardcoded later
        content = "<p> There are %s places that match your description, here are 4 of them </p>" %(len(info))

        numTo = 4

        if len(info) < 4:
                numTo = len(info)

        for i in range(listIndex,numTo + listIndex):
                content += "<div>"
                content += "<p>name: %s</p>" %(info[i]['Name'])
                content += "<p>specilization: %s</p>" %(info[i]['sp_name'])
                content += "<p>Address: %s</p>" %(info[i]['Address'])
                if info[i]['Info_found'] != "" and info[i]['Info_found'] != None:
                        content += "<p> Website:<a href= \"%s\"> Visit their Website Now!</a></p>" %(info[i]["Info_found"])
                if info[i]['Phone No'] != "" and info[i]['Phone No'] != None:
                        content += "<p>%s</p>" %(info[i]["Phone No"])
                


                content += "<br></div>"


        return content


def buildResponseOutput(info):
        content = "<div><p> Of Course! Here is some more info! <p>"
        print("BuildResponseData",info)
        for key,value in info.items():
                content += "<p>%s: %s </p>" %(key,value)

        content += "</div>"

        return content