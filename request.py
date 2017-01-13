#!/usr/bin/python3
# 12/01/17 on sydney_manjaro@sydney-manjaro

import requests
import subprocess
import json

#with urllib.request.urlopen('http://127.0.0.1:8000') as f:
#    print(f.read(200))

def sendHello(status, shortLog):

    uniqID = subprocess.check_output(['./getUniqID.sh']).decode('ascii')

    uniqID = uniqID.replace('\n', '')
    uniqID = uniqID.replace(" ", '')
    print(uniqID)
    
    
    info = subprocess.check_output(['uname', '-a']).decode('ascii')
    info = info.replace("\n", "")

    # If the rasp detects probleme on its own, it send status=1, otherwise 2
    userdata = {'id': uniqID, "status": status, "info": info, "shortLog":shortLog}
    resp = requests.post('http://127.0.0.1:8000/wthit/whatsup', data=userdata)
    #resp = requests.get('http://127.0.0.1:8000')
    
    print(resp.text)
    return int(resp.text)
    
def main():
    retry = 2;  # max: 2 loop
    status = 2
    shortLog = ""
    while(retry):
        code = sendHello(status, shortLog)
        if (code >= 500):
            # If there is a server error it will re-try only at the next loop
            retry = False
        elif (code >= 400):
            # Client error
            retry -= 1
            status = 1
            shortLog = "Code lors de la derniere tantative de connexion: " + code
        elif(code >= 300):
            print("Unexpected redirection code")
            retry = False
        elif(code >= 200):
            print("Ok")
            retry = False
        elif(code >= 100):
            print("Ok")
            retry = False
        else:
            print("Unexpected code")
            retry -= 1
            
if __name__ == "__main__":
    main()
    
    
