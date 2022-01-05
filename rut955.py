import requests
import json

# https://realpython.com/api-integration-in-python/


class Rut955:
    def __init__(self):
        self.api_url = "http://10.1.1.254/ubus"

    def getSession(self, userName, password):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    "00000000000000000000000000000000", "session", "login",
                    {
                        "username": userName,
                        "password": password
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['ubus_rpc_session']
            else:
                return ""
        except:
            print("FAILED: ", "No response")

        return ""

    def getGsmRSSI(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "exec",
                    {
                        "command": "gsmctl",
                        "params":
                        [
                            "-q"
                        ]
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['stdout']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getIP(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "exec",
                    {
                        "command": "gsmctl",
                        "params":
                        [
                            "-pwwan0"
                        ]
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['stdout']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getNetworkConfig(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "exec",
                    {
                        "command": "cat",
                        "params":
                        [
                            "/etc/config/network"
                        ]
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['stdout']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getWifiClient(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "iwinfo", "assoclist",
                    {
                        "device": "wlan0"
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getWifiInfo(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "iwinfo", "info",
                    {
                        "device": "wlan0"
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getManufacturerInfo(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "exec",
                    {
                        "command": "mnf_info", "params": ["name", "sn", "mac"]
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['stdout']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getGps(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "exec",
                    {
                        "command": "gpsctl", "params": ["-ix"]
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['stdout']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def getFw(self, sessionId):
        try:
            body = {
                "jsonrpc": "2.0", "id": 1, "method": "call", "params":
                [
                    sessionId, "file", "read",
                    {
                        "path": "/etc/version"
                    }
                ]
            }

            response = requests.post(self.api_url, json=body)
            if (response.status_code == 200):
                responseJson = response.json()
                return responseJson['result'][1]['data']
            else:
                return ""
        except:
            print("FAILED: ", "No response")
        return ""

    def run(self):
        print(self.api_url)


if __name__ == "__main__":
    rut955 = Rut955()
    sessionId = rut955.getSession("root", "Ampang2020")
    if sessionId == "":
        print("FAILED")
    else:
        print("Session ", sessionId)
        gsmSignal = rut955.getGsmRSSI(sessionId)
        print("GSM Signal ", gsmSignal)
        networkConfig = rut955.getNetworkConfig(sessionId)
        print("Network ", networkConfig)
        wifiClient = rut955.getWifiClient(sessionId)
        print("WifiClient ", wifiClient)
        wifiInfo = rut955.getWifiInfo(sessionId)
        print("WifiInfo ", wifiInfo)
        manufacturer = rut955.getManufacturerInfo(sessionId)
        print("Manufacturer ", manufacturer)
        gps = rut955.getGps(sessionId)
        print("GPS ", gps)
        fw = rut955.getFw(sessionId)
        print("FW ", fw)
        ip = rut955.getIP(sessionId)
        print("IP ", ip)


        