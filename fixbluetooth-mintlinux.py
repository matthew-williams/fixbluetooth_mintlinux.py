#!/usr/bin/env python
# Title:    Python 2.7 BT and ATH10K Drivers for Mint
# Author:   Matthew Williams
# Date:     01/12/2018
import os
import sys
import platform
import time
import subprocess
#
# VARIABLE DEFINITION
#
current_time = time.strftime("%H:%M:%S") # time variable
current_date = time.strftime("%d-%m-%Y") # date variable
dist_name = platform.linux_distribution()[0] # For Linux Distro's store the distribution name
dist_version = platform.linux_distribution()[1] # For Linux Distro's store the version number
script_path = os.path.abspath(os.path.dirname(sys.argv[0])) # Location script is ran from. *** NOT USED ***
debug_flag = False # variable to call when you need to debug *** NOT USED ***
intro_text = """
##################################################################
# Title:    Python 2.7 BT and ATH10K Drivers for Mint
# Author:   Matthew Williams
# Date:     01/12/2018
# Latest Update:   01/12/2018
#
# Description: Resolve issues with Bluetooth and ATH10K kernel drivers
"""
#
# END OF VARIABLE DEFINITION
#
#
# FUNCTIONS DEFINITION
#
def check_os(): # Function to determine OS and whether or not to continue
    from sys import platform
    if platform == "linux" or platform == "linux2": # Linux...
        print (intro_text)
        print ("Your OS:"),
        print (dist_name),
        print (dist_version)
        return()
            # End Linux...
    elif platform == "darwin": #OS X...
        print("Your OS is MAC")
        print("This script is for Linux Machines only...")
        exit_script(0)
            # End OS X...
    elif platform == "win32": # Windows...
        print("Your OS is Windows")
        print("This script is for Linux Machines only...")
        exit_script(0)
            # End Windows...
    else:
        print("I cannot determine your Operating System type...") # tell user that the OS cannot be determined and quit
        exit_script(0)

def exit_script(exit_code): # Function to exit script, will build exception handling in the future
    print("Exiting script.")
    sys.exit(exit_code)

def fixbt():
    try:
        if os.path.exists("/home/adminlocal/Downloads/Firmware/ath10k-firmware-master/QCA6174/"):
            rsync_output = subprocess.check_output("sudo rsync -rav /home/adminlocal/Downloads/Firmware/ath10k-firmware-master/QCA6174/ /lib/firmware/ath10k/QCA6174/", shell=True)
        else:
            print("Firmware/ath10k-firmware-master/QCA6174/ not found!")
            return()
    except:
        print(rsync_output)
        print("rsync_output Failed")
        return()
    try:
        chmod_output = subprocess.check_output("sudo chmod 755 -R /lib/firmware/ath10k/QCA6174/ && sudo chown root:root -R /lib/firmware/ath10k/QCA6174/ && sudo chmod +x -R /lib/firmware/ath10k/QCA6174/", shell=True)
    except:
        print(chmod_output)
        print("chmod_output Failed")
        return()
    subprocess.call("sudo modprobe -r btrtl hci_uart btintel btqca bnep btbcm btusb", shell=True)
    subprocess.call("sudo modprobe -v btrtl hci_uart btintel btqca bnep btbcm btusb", shell=True)
    try:
        ath10kdisable_output = subprocess.check_output("sudo modprobe -r ath10k_pci", shell=True)
    except:
        print(ath10kdisable_output)
        print("ath10kdisable_output Failed")
        return()
    try:
        ath10kenable_output = subprocess.check_output("sudo modprobe -v ath10k_pci", shell=True)
    except:
        print(ath10kenable_output)
        print("ath10kenable_output Failed")
        return()
    try:
        systembtenable_output = subprocess.check_output("sudo systemctl enable bluetooth.service", shell=True)
    except:
        print(systembtenable_output)
        print("systembtenable_output Failed")
        return()
    try:
        initbtrestart_output = subprocess.check_output("sudo /etc/init.d/bluetooth restart", shell=True)
    except:
        print(initbtrestart_output)
        print("initbtrestart_output Failed")
        return()
    try:
        initbtstatus_output = subprocess.check_output("sudo /etc/init.d/bluetooth status|grep running", shell=True)
    except:
        print(initbtstatus_output)
        print("initbtstatus_output Failed")
        return()
    subprocess.call("sudo reboot", shell=True)
#
# END OF FUNCTIONS DEFINITION
#
#
# PROGRAM DEFINITION
#
check_os()
fixbt()
exit_script(0)
#
# END OF PROGRAM DEFINITION
#
