#!/usr/bin/python
import subprocess

def sysUpdate():
    # Function number: 1
    stdout = open("update.log", 'w')
    command = ['apt', 'update']
    subprocess.call(command, stdout==stdout)
    
    return 0
    
def sysUpgrade():
    # Function number: 2
    sysUpdate()
    stdout = open("upgrade.log", 'w')
    command = ['apt', '--assume-yes', 'upgrade']
    subprocess.call(command, stdout==stdout)
    
    return 0

def sysDitUpgrade():
    # Function number: 3
    sysUpdate()
    sysUpgrade()
    stdout = open("dist-upgrade.log", 'w')
    command = ['apt', '--assume-yes', 'dist-upgrade']
    subprocess.call(command, stdout==stdout)
    
    return 0

def sysReboot():
    # Function number: 10
    subprocess.call(['reboot'])
    
    return 0
