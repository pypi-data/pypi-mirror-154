import requests
import json
from time import sleep

class serviceStatus :
    def update(team_input, service_name, time_loop) :
        service_data = json.dumps({"team": team_input, "name": service_name})
        url = 'https://buildingapimgmt.azure-api.net/altotech-status/updateStatus'
        while True: 
            if team_input not in ["Dev", "IoT", "Data Sci", "CV"] :
                print("Team name is invalid, please enter valid team name : 'Dev','IoT','Data Sci','CV'")
                return
            res = requests.patch(url, data=service_data)
            if (res.status_code == 200) :
                print("Update service status successfully!")
            if (res.status_code == 500) :
                print("Error, something went wrong!")
                print(res.text)
            sleep(time_loop * 60)