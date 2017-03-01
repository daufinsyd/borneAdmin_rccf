#!/usr/bin/python
import subprocess
import sys

def setMaxVol(maxVol):
    sys.stdout = open("actions.log", 'a')
    print("[II] Set maxVol to:", str(maxVol))
    command = ['amixer', 'set', 'Master', '50%']
    subprocess.call(command, stdout=stdout)

    return 0

def sysUpdate():
    # Function number: 1
    sys.stdout = open("actions.log", 'a')
    print("[II] Update", str(maxVol))
    stdout = open("update.log", 'w')
    command = ['apt', 'update']
    subprocess.call(command, stdout=stdout)
    
    return 0
    
def sysUpgrade():
    # Function number: 2
    sys.stdout = open("actions.log", 'a')
    print("[WW] Upgrade", str(maxVol))
    sysUpdate()
    stdout = open("upgrade.log", 'w')
    command = ['apt', '--assume-yes', 'upgrade']
    subprocess.call(command, stdout=stdout)
    
    return 0

def sysDitUpgrade():
    # Function number: 3
    sys.stdout = open("actions.log", 'a')
    print("[WW] Dist upgrade", str(maxVol))
    sysUpdate()
    sysUpgrade()
    stdout = open("dist-upgrade.log", 'w')
    command = ['apt', '--assume-yes', 'dist-upgrade']
    subprocess.call(command, stdout=stdout)
    
    return 0

def sysReboot():
    # Function number: 10
    sys.stdout = open("actions.log", 'a')
    print("[WW] Reboot", str(maxVol))
    subprocess.call(['reboot'])
    
    return 0
