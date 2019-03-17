import os
import sys
import string
import subprocess
import xml.etree.ElementTree as ET
import datetime
import re

"""
Global Variable: today in format of yyyy-mm-dd
"""
today = datetime.date.today().strftime('%Y-%m-%d')

def get_xml():
    """
    Get battery report from Windows command prompt by using powercfg 
    and export the report to XML file
    
    @param: none
    @return: latest battery_report.xml in current directory
    @throw: none
    """
    subprocess.call('powercfg /batteryreport /output .\\battery_report.xml /XML /Duration 3')

def parse_xml():
    """
    Parse the battery report XML file by representing the whole document as a tree 
    and get the nearest day battery usage history. Convert the active AC charging time 
    to hours as a float number and use corresponding computer consumption to convert to kwh

    @param: none
    @return: kwh: float
    @throw: none
    """
    tree = ET.parse('battery_report.xml')
    root = tree.getroot()
    
    history = root[5]
    i = 0
    active = 0
    kwh = 0
    # loop until latest entry found
    while True:
        #use EndDate to find "today"
        endt = history[i].attrib['EndDate'][:10]
        if endt == today:
            active = history[i].attrib['ActiveAcTime']
            atime = re.split('PT|H|M|S',active)
            time = float(atime[1])+float(atime[2])/60
            # 240 is Alienware 17 R5's power consumption specification 240 watt/h
            kwh = time * 240 / 1000
            break
        i += 1
    return kwh

if __name__ == "__main__":
    get_xml()
    x = parse_xml()
    print(x)
