from pydoc import resolve
import requests
import json

# https://realpython.com/api-integration-in-python/


class Rut955:
    def __init__(self):
        self.api_url = "http://10.1.1.254/ubus"

        self.sms_api_url = "http://10.1.1.254/cgi-bin/"
        self.sms_user = 'rtu01'
        self.sms_password = 'hdls2019'

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
            print("FAILED 1: ", "No response")

        return ""

    #ref: https://wiki.teltonika-networks.com/view/RUT955_Mobile_Utilities

    def smsGetList(self):
        #http://10.1.1.254/cgi-bin/sms_list?username=rtu01&password=hdls2019
        try:
            url = self.sms_api_url + 'sms_list?username=' + self.sms_user + '&password=' + self.sms_password
            response = requests.get(url)
            if (response.status_code == 200):
                messages = []
                lines = response.text.splitlines()
                line_index = ""
                line_date = ""
                line_sender = ""
                line_text = ""
                line_status = ""
                for line in lines:
                    if line.startswith('Index:'):
                        line_index = line[7:]
                    if line.startswith('Date:'):
                        line_date = line[6:]
                    if line.startswith('Sender:'):
                        line_sender = line[8:]
                    if line.startswith('Text:'):
                        line_text = line[6:]
                    if line.startswith('Status:'):
                        line_status = line[8:]
                    if line.startswith('------------------------------'):
                        messages.append({
                            "index": line_index,
                            "date": line_date,
                            "sender": line_sender,
                            "text": line_text,
                            "status": line_status
                        })
                        line_index = ""
                        line_date = ""
                        line_sender = ""
                        line_text = ""
                        line_status = ""
                
                return messages

            else:
                return "FAILED"
        except:
            print("FAILED 2: ", "No response")
        return ""

        pass

    def smsRead(self, number):
        # Read mobile message	
        # http://192.168.1.1/cgi-bin/sms_read?username=user1&password=user_pass&number=1
        try:
            url = self.sms_api_url + 'sms_read?username=' + self.sms_user + '&password=' + self.sms_password + '&number=' + str(number)
            response = requests.get(url)
            if (response.status_code == 200):
                lines = response.text.splitlines()
                if lines.length == 0:
                    return ""
                line_index = ""
                line_date = ""
                line_sender = ""
                line_text = ""
                line_status = ""
                messages = None
                for line in lines:
                    if line.startswith('Index:'):
                        line_index = line[7:]
                    if line.startswith('Date:'):
                        line_date = line[6:]
                    if line.startswith('Sender:'):
                        line_sender = line[8:]
                    if line.startswith('Text:'):
                        line_text = line[6:]
                    if line.startswith('Status:'):
                        line_status = line[8:]

                messages = {
                    "index": line_index,
                    "date": line_date,
                    "sender": line_sender,
                    "text": line_text,
                    "status": line_status
                }
                
                return messages
            else:
                return "FAILED"
        except Exception as e:
            print("FAILED: ", e)
        return ""

    def smsSendGroup(self, smsGroup, message):
        #Send mobile message to a group	http://192.168.1.1/cgi-bin/sms_send?username=user1&password=user_pass&group=group_name&text=testmessage
        pass

    def smsTotal(self):
        ##View mobile messages total	http://192.168.1.1/cgi-bin/sms_total?username=user1&password=user_pass
        try:
            url = self.sms_api_url + 'sms_total?username=' + self.sms_user + '&password=' + self.sms_password
            response = requests.get(url)
            if (response.status_code == 200):
                lines = response.text.splitlines()
                line_used = ""
                line_total = ""
                for line in lines:
                    if line.startswith('Used:'):
                        line_used = line[6:]
                    if line.startswith('Total:'):
                        line_total = line[7:]
                return {
                    "used": line_used,
                    "total": line_total,
                }
            else:
                return ""
        except Exception as e:
            print("Exception: ", e)
        return ""


    def smsDeleteAll(self):
        try:
            messages = self.smsGetList()
            for message in messages:
                self.smsDelete(message['index'])
        except Exception as e:
            print("Exception: ", e)
        return ""


    def smsDelete(self, number):
        #Delete mobile message	http://192.168.1.1/cgi-bin/sms_delete?username=user1&password=user_pass&number=1
        try:
            url = self.sms_api_url + 'sms_delete?username=' + self.sms_user + '&password=' + self.sms_password + '&number=' + str(number)
            response = requests.get(url)
            if (response.status_code == 200):
                return response.text
            else:
                return ""
        except Exception as e:
            print("Exception: ", e)
        return ""


    def smsSend(self, smsTo, message):
        try:
            #http://10.1.1.254/cgi-bin/sms_send?username=rtu01&password=hdls2019&number=%2B60192563019&text=Testing_with_plus
            url ='http://10.1.1.254/cgi-bin/sms_send?username=rtu01&password=hdls2019&number=%2B6' + smsTo + '&text=' + message
            response = requests.get(url)
            if (response.status_code == 200):
                return "OK"
            else:
                return "FAILED"
        except:
            print("FAILED 3: ", "No response")
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
            print("FAILED 4: ", "No response")
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
            print("FAILED 5: ", "No response")
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
            print("FAILED 6: ", "No response")
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
            print("FAILED 7: ", "No response")
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
            print("FAILED 8: ", "No response")
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
            print("FAILED 9: ", "No response")
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
            print("FAILED 10: ", "No response")
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
            print("FAILED 11: ", "No response")
        return ""

    def run(self):
        print(self.api_url)


if __name__ == "__main__":
    rut955 = Rut955()
    list = rut955.smsGetList()
    print('sms list', list)
    exit()

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


    # print('list', list)

    # read = process.smsRead(2)
    # print('read', read)

    # total = process.smsTotal()
    # print('total', total)

    # delete = process.smsDeleteAll()
    # print('delete', delete)



    # read = process.smsRead(2)
    # print('read', read)

    # total = process.smsTotal()
    # print('total', total)
        