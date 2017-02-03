#!/usr/bin/python3
# 12/01/17 on sydney_manjaro@sydney-manjaro

import requests
import subprocess
import json

import commands

WORK_DIR = '/home/sydney_manjaro/tmp'


def getUID():
    uniqID = subprocess.check_output(['./getUniqID.sh']).decode('ascii')

    uniqID = uniqID.replace('\n', '')
    uniqID = uniqID.replace(" ", '')
    print(uniqID)
    
    return uniqID

def sendHello(status, shortLog):
    uniqID = getUID()
    
    info = subprocess.check_output(['uname', '-a']).decode('ascii')
    info = info.replace("\n", "")

    # If the rasp detects probleme on its own, it send status=1, otherwise 2
    userdata = {'id': uniqID, "status": status, "info": info, "shortLog":shortLog}
    resp = requests.post('http://127.0.0.1:8000/wthit/whatsup', data=userdata)
    
    print("Hello svr", resp.text)
    return int(resp.text)
    
def askServer():
    # Ask server wether there is something to do.
    
    data = {'uuid': 1}#getUID()}
    pendingActions = requests.post('http://127.0.0.1:8000/wthit/imbored', data=data)
    unattendedActions = []
    
    print("Actions", pendingActions)
    # pendingAction: if no action first element is the status return code
    if len(pendingActions.json()):
        print(pendingActions.json()[1])
        pendingActions = pendingActions.json()
        
        # Save pendingActions whenever the terminal unexpectedly shutdown
        with open(WORK_DIR + '/pending.json', 'w') as outfile:
            json.dump(pendingActions, outfile)
        
        completedActions = {}  # dict of completed actions with their status
        
        # Processing actions
        for action in pendingActions:
            cmdStatus = -1  # Return code of the issued command
            if(action['codeCmd'] == 0):
                print('[II] Exécution d\'une commande personnalisée', action['cmd'])
            else:
                if(action['cmd'] == 1):
                    cmdStatus = commands.sysUpdate()
                elif(action['cmd'] == 2):
                    cmdStatus = commands.sysUpgrade()
                elif(action['cmd'] == 3):
                    cmdStatus = commands.sysDistUpgrade()
                elif(action['cmd'] == 10):
                    cmdStatus = commands.reboot()
            
            # Remove accomplished action from pendingActions and add it to completedActions (with its return code)
            completedActions[action['id']] = cmdStatus
            pendingActions =  [k for k in pendingActions if int(k['id']) != int(action['id'])]
            with open(WORK_DIR + '/pending.json', 'w') as outfile:
                json.dump(pendingActions, outfile)
            
            print('\nPending actions: ', pendingActions, '\nCompleted actions: ', completedActions)
            
    
    # Send back to server all completed actions
    

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
            
    askServer()
     
if __name__ == "__main__":
    main()
    
    
