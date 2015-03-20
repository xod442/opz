#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    imc_dev.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Gets the first 10K devices from an IMC server and makes a report
#  
#
#------Might not need this but please they are handy------------------------ 
#
# Do the imports!!!! 
#----------------------If you dont have it use "apt-get install (name)"

import sys 
import subprocess
import cgi
import cgitb; cgitb.enable()
import hpsdnclient as hp
import sqlite3
import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
imc_server = "10.132.0.106:8080"
imc_user = "admin"
imc_passw = "admin"
"""
apSwitchIp = "0.0.0.0"
apPort = "Gigabit 1/0/1"
"""
# Set script variables
data = []
data1 = []
h_url =  "http://"                      	                # Prefix for URL
t_url = "/imcrs/wlan/clientInfo/queryAllClientBasicInfo"    	# Append to url set size for amoutn of devices to pull 10K will gett all entries from most servers
count = 0                               	                #  Another counter


#------------------------------------------------------------------------------
#         Get IMC device information
#-----------------------------------------------------------------------------

auth=HTTPDigestAuth(imc_user,imc_passw)
#	Prep the IP for API use and build API url
api_url = "%s%s%s" % (h_url, imc_server, t_url)
# Now HTTP get to IMC for the device information...if it's there
r = requests.get(api_url, auth=auth)
if r.status_code == 200:
   #   Collect entries and write them to the dpid table in the glarn db
   #print "Lookiong in IMC...."
   tree = xml.fromstring(r.content)
  
   for node in tree.iter():
    
     data.append(node.text)
     
     # If node.tag is the parent tag clear the data[] array and iterate
     if node.tag == 'list':
         data = []
   
     
     if node.tag == 'acDevId':
         upTime = data[6]
         apLabel = data[11]
         signalStrength = data[7]
         ss = int(signalStrength)
         print ss
         if (ss < -1 and ss > -50):
	   print "Very HAPPY!!!"
	 if (ss < -50 and ss > -75):
	   print "Happy"
         if (ss < -75 and ss > -100):
	   print "Very unhappy"
         ipAddress = data[2]
         mac = data[1]
         userName = data[3]
         apIpAddress = data[12]
         acLabel = data[14]
         ssid = data[5]  
         
         #------------------------------------------------------------------------
         # Real time locate mac for access point to determinew switch connections
         #------------------------------------------------------------------------
                 
	 #print "--%s, --%s, --%s, --%s, --%s, --%s, --%s, --%s, --%s" % (upTime,apLabel,signalStrength,ipAddress,mac,userName,acLabel,ssid,apIpAddress)
         
         count = count + 1
         data = []
