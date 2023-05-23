

def buildOutput(info):
        if info == None:
                return "<p> No matches were found </p>"
        
        # Change this to not be hardcoded later
        content = "<p> There are %s places that match your description, here are 4 of them </p>" %(len(info))

        for i in range(0,4):
                content += "<div>"
                content += "<p>name: %s</p>" %(info[i]['Name'])
                content += "<p>specilization: %s</p>" %(info[i]['sp_name'])
                content += "<p>Address: %s</p>" %(info[i]['Address'])
                if info[i]['Info_found'] != "" and info[i]['Info_found'] != None:
                        content += "<p> Website:<a href= \"%s\"> Visit their Website Now!</a></p>" %(info[i]["Info_found"])

                content += "</div>"

        return content

                