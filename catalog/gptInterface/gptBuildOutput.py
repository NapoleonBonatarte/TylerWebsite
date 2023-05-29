


def listToString(list, numToStart, numToEnd):



        retString = ""
        if len(list) < numToEnd:
                numToEnd = len(list)
        for i in range(numToStart,numToEnd):
                retString += list[i]


        print("FROM LIST TO STRING: ", retString)
        return retString


def buildLocationOutput(info, listIndex):
        print("LIST INDEX", listIndex)
        if info == None:
                return "<div class='columnRight'><p class='columnTextRight'> Unfortunately I was not able to find any places that fit your criteria. </p></div>"
        if len(info) == 0:
                return "<div class='columnRight'><p class='columnTextRight'> Unfortunately I was not able to find any places that fit your criteria. </p></div>"
        
        # Change this to not be hardcoded later

        retList = []

        numTo = 4
        #content = "<div class='columnRight'><p class='columnTextRight'>There are %s places that match your description, here are %s of them</p></div>" %(len(info), numTo)
        content = "<div class='columnRight'><p class='columnTextRight'>There are %s places that match your description</p></div>" %(len(info))

        for i in range(0,len(info)):
                content += "<div class='columnRight'> <div class='columnTextRight'>"
                content += "<p>%s</p>" %(info[i]['Name'])
                content += "<p>Specilization: %s</p>" %(info[i]['sp_name'])
                content += "<p>Address: %s</p>" %(info[i]['Address'])
                if info[i]['Info_found'] != "" and info[i]['Info_found'] != None:
                        content += "<p> Website:<a href= \"%s\"> Visit their Website Now!</a></p>" %(info[i]["Info_found"])
                if info[i]['Phone No'] != "" and info[i]['Phone No'] != None:
                        content += "<p>%s</p>" %(info[i]["Phone No"])
                


                content += "</div></div><br>"

                content += "<div>&nbsp<br></div>"

                retList.append(content)
                content = ""


        return retList


def buildResponseOutput(info):
        content = "<div class='columnRight'><div class='columnTextRight'>"
        content += "<p>%s</p>" %(info)
        content += "</div></div>"

        content += "<div>&nbsp<br></div>"

        return content