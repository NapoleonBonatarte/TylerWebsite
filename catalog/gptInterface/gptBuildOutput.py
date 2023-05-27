

def buildLocationOutput(info, listIndex):
        print("LIST INDEX", listIndex)
        if info == None:
                return "<p> No matches were found </p>"
        
        # Change this to not be hardcoded later

        numTo = 4

        if len(info) < 4:
                numTo = len(info)

        content = "<div class='columnRight'><p class='columnTextRight'>There are %s places that match your description, here are %s of them</p></div>" %(len(info), numTo)

        for i in range(0,numTo + listIndex):
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


        return content


def buildResponseOutput(info):
        content = "<div class='columnRight'><div class='columnTextRight'>"
        content += "<p>%s</p>" %(info)
        content += "</div></div>"

        content += "<div>&nbsp<br></div>"

        return content