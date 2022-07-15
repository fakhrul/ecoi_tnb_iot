import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
# https://realpython.com/api-integration-in-python/


class DbApi:
    def __init__(self):
        self.api_url = os.getenv('API_URL')
        self.token = ""
        self.user = ""

    def getSession(self, userName, password):
        try:
            body = {
                "email" : userName,
                "password": password
            }
            url = self.api_url + "/Account/login"

            response = requests.post( url, json=body, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                responseResult = responseJson['result']
                self.token = responseResult['token']
                self.user = responseResult['userName']
                return responseResult
            else:
                return ""
        except  Exception as e:
            print("FAILED: ", e)

        return ""
    def getConfiguration(self):
        try:
            body = {}
            
            url = self.api_url + "/Configurations/ByLatest"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            response = requests.get(url, json=body, headers=headers, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                responseResult = responseJson['result']
                return responseResult
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getEquipementStatus(self):
        try:
            body = {}
            
            url = self.api_url + "/EquipmentStatuses/ByLatest"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            response = requests.get(url, json=body, headers=headers, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                responseResult = responseJson['result']
                return responseResult
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getPendingCommand(self):
        try:
            body = {}
            
            url = self.api_url + "/Commands/ByPending"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            response = requests.get(url, json=body, headers=headers, verify=False)
            print('response',response)
            if (response.status_code == 200):
                try:
                    responseJson = response.json()
                    print('responseJson',responseJson)
                    responseResult = responseJson['result']
                    print('responseResult',responseResult)
                    return responseResult
                except Exception as e:
                    return None
                # return responseResult['sirenMode']
            else:
                return None
        except:
            print("FAILED: ", "No response")
        return None

    def updatePendingCommand(self):
        try:
            body = {}
            
            url = self.api_url + "/Commands/UpdatePending"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            response = requests.post(url, json=body, headers=headers, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def setSirenCommand(self, appName, state):
        try:
            url = self.api_url + "/Commands"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            body = {
                "appName" : appName,
                "sirenMode": state
            }

            response = requests.post(url, json=body, headers=headers, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""
    def addEquipmentStatus(self, equipment):
        try:
            url = self.api_url + "/EquipmentStatuses"
            headers =  {
                "Authorization":"Bearer " + self.token
            }

            body = equipment

            response = requests.post(url, json=body, headers=headers, verify=False)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def run(self):
        print(self.api_url)


if __name__ == "__main__":
    dbApi = DbApi()
    while True:
        result = dbApi.getSession("admin@email.com", "Qwerty@123")

        sirenCommand = dbApi.getPendingCommand()
        print(sirenCommand)

        if sirenCommand != "":
            # do siren process
            print('do siren process')

            res = dbApi.updatePendingCommand()

            equipmentStatus = {
                "gpsLatitude" : "1",
                "gpsLongitude" : "2",
                "batteryVoltage" : "3",
                "solarVoltage" : "4",
                "rtuTemperature" : "5",
                "gsmSignal" : "6",
                "sirenMode" : sirenCommand,
            }
            dbApi.addEquipmentStatus(equipmentStatus)

            # verify
            res = dbApi.getPendingCommand()
            print("pending", res)
        else:
            print('no pending')

    # if sessionId == "":
    #     print("FAILED")
    # else:
    #     print("Session ", sessionId)
    #     gsmSignal = rut955.getGsmRSSI(sessionId)
    #     print("GSM Signal ", gsmSignal)
    #     networkConfig = rut955.getNetworkConfig(sessionId)
    #     print("Network ", networkConfig)
    #     wifiClient = rut955.getWifiClient(sessionId)
    #     print("WifiClient ", wifiClient)
    #     wifiInfo = rut955.getWifiInfo(sessionId)
    #     print("WifiInfo ", wifiInfo)
    #     manufacturer = rut955.getManufacturerInfo(sessionId)
    #     print("Manufacturer ", manufacturer)
    #     gps = rut955.getGps(sessionId)
    #     print("GPS ", gps)
    #     fw = rut955.getFw(sessionId)
    #     print("FW ", fw)
    #     ip = rut955.getIP(sessionId)
    #     print("IP ", ip)


        