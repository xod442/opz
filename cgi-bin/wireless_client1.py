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
#  Initial release - Make a report with wierless client info and real time location api's
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
import time
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------

form = cgi.FieldStorage()
imc_server = form.getvalue('imc_server')
imc_user = form.getvalue('imc_user')
imc_passw = form.getvalue('imc_passw')
#imc_server = "10.132.0.107:8080"
#imc_user = "admin"
#imc_passw = "admin"
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
#Start the return page
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title> Wookieware.com</title>"
print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
print "</head>"
print "<body>"
print "<h1> <img src=\"../../images/report.png\" width=\"125\" height=\"60\">   IMC API reporting</h1>" 
print "<HR> "
print "<h3> Wireless Client Experience</h3>"
print "<p>This is a listing of wireless clients and their signal strength. Shows AP association and where the AP is connected to the physical switch</p>"
print "<hr>"
print "<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">"
print "<tr>"
print "<td>Online Seconds</td>" 
print "<td>Access Point</td>"  
print "<td>RSSI</td>"
print "<td>Client Ip Address</td>"
print "<td>Client Mac</td>"
print "<td>Username</td>" 
print "<td>WLC</td>"  
print "<td>SSID</td>" 
print "<td>Access Point IP</td>" 
print "<td>AP Switch Ip</td>" 
print "<td>Ap Port</td>"  
print "</tr>"

#------------------------------------------------------------------------- 

#import pdb; pdb.set_trace()
# Auth for imc
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
   
     
     if node.tag == 'acDevId':		# You have reached the bottom of the elemenet, get out!
         upTime = data[6]
         upTime = int(upTime)
         upTime = time.strftime('%H:%M:%S', time.gmtime(upTime))
         apLabel = data[11]
         signalStrength = data[7]
         
         
         # Check the mood of the client based on the Received Signal Strength Indicator
         
         ss = int(signalStrength)

         if (ss < -1 and ss > -50):
	   ss_out = "<img src=\"../../images/very_happy.png\" width=\"30\" height=\"30\">"
	 
	 elif (ss < -50 and ss > -75):
	   ss_out = "<img src=\"../../images/happy.png\" width=\"30\" height=\"30\">"
         
         else:
	   ss_out = "<img src=\"../../images/unhappy.png\" width=\"30\" height=\"30\">"
         
         
         
         ipAddress = data[2]
         mac = data[1]
         userName = data[3]
         if not userName:
	   userName = "No Auth"
         apIpAddress = data[12]
         acLabel = data[14]
         if  not acLabel:
	   acLabel = "Autonomous"
         ssid = data[5]  
         
         #------------------------------------------------------------------------
         # Real time locate mac for access point to determinew switch connections
         #------------------------------------------------------------------------
         
         auth=HTTPDigestAuth(imc_user,imc_passw)        	#Prep the IP for API use and build API url
						  
						 
	 ip_url = "/imcrs/res/access/realtimeLocate?&value=%s" % (apIpAddress)
	 
	 api_url = "%s%s%s" % (h_url, imc_server, ip_url)     	# Now HTTP get to IMC for the access point location information...if it's there
						 
	 r = requests.get(api_url, auth=auth)
	 if r.status_code == 200:				#   Collect entries and find the switch information
	     
	     tree1 = xml.fromstring(r.content)
	    
	     apIpAddress = tree1[0][0].text
	     apSwitchIp = tree1[0][2].text
	     apPort = tree1[0][3].text
	     
	     # Print line to the browser
	     
	     print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (upTime,apLabel,ss_out,ipAddress,mac,userName,acLabel,ssid,apIpAddress,apSwitchIp,apPort)
         count = count + 1
         data = []

#---------------------------------
#         Finish return
#---------------------------------------------------------------------------
print "</table>"
print "<FORM method='post' ACTION=\"./imc_rpt.py\">"
print "<hr>"
print "<img src=\"../../images/very_happy.png\" width=\"30\" height=\"30\"> = Very Happy <img src=\"../../images/happy.png\" width=\"30\" height=\"30\"> = Happy <img src=\"../../images/unhappy.png\" width=\"30\" height=\"30\"> = Unhappy"
print "<p>There were a total of %s records actually found</p>" % (count)
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Home\"></center>"
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "</form>"
print "<footer>" 
print "<a href=\"/imc_dev.html\">BACK</a>" 
print "<center><font face=\"Arial\" size=\"1\">IMC Solutions From WookieWare 2014</font></center>"
print "</footer>"
print "</body>"
print "</html>"



