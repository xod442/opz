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
import xml.etree.ElementTree as ET

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
imc_server = "10.132.0.106:8080"
imc_user = "admin"
imc_passw = "admin"
apMacAddress = "2c:41:38:db:bd:58"
# Set script variables
data = []
data1 = []
h_url =  "http://"   
mac_url = "/imcrs/res/access/realtimeLocate?type=1&value=%s" % (apMacAddress)                   	                # Prefix for URL
count = 0                               	                #  Another counter

         
         #------------------------------------------------------------------------
         # Real time locate mac for access point to determinew switch connections
         #------------------------------------------------------------------------
         
auth=HTTPDigestAuth(imc_user,imc_passw)        	#Prep the IP for API use and build API url
						  
						 
						 


api_url = "%s%s%s" % (h_url, imc_server, mac_url)     	# Now HTTP get to IMC for the location information...if it's there
	 
print api_url
						 
r = requests.get(api_url, auth=auth)

if r.status_code == 200:				#   Collect entries and find the switch information
							    
  root = ET.fromstring(r.content)
  mac = root[0][0].text
  devid = root[0][1].text
  devip = root[0][2].text
  ifdesc = root[0][3].text
  ifindex = root[0][4].text
  
  print "--%s, --%s, --%s, --%s, --%s" % (mac, devid,devip,ifdesc,ifindex)
	    
"""
for node in tree1.iter():
    
    data1.append(node.text)
    print node.tag 
    
	      if node.tag == 'list':					# If node.tag is the parent tag clear the data[] array and iterate
		data1 = []
   
     
	      if node.tag == 'ifIndex':
		apSwitchIp = data1[3]
		apPort = data1[4]
		print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (upTime,apLabel,signalStrength,ipAddress,mac,userName,acLabel,ssid,apSwitchIp,apMacAddress,apPort)
         count = count + 1
         data = []
"""
#---------------------------------
#         Finish return
#---------------------------------------------------------------------------



