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

form = cgi.FieldStorage()
imc_server = form.getvalue('imc_server')
imc_user = form.getvalue('imc_user')
imc_passw = form.getvalue('imc_passw')

apSwitchIp = "0.0.0.0"
apPort = "Gigabit 1/0/1"

# Set script variables
data = []
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
print "<p>This is a listing of the 1st 10,000 records found in IMC</p>"
print "<hr>"
print "<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">"
print "<tr>"
print "<td>Online</td>" 
print "<td>Access Point</td>"  
print "<td>RSSI</td>"
print "<td>Client Ip Address</td>"
print "<td>Client Mac</td>"
print "<td>Username</td>" 
print "<td>WLC</td>"  
print "<td>SSID</td>"  
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
   
     
     if node.tag == 'acDevId':
         upTime = data[6]
         apLabel = data[11]
         signalStrength = data[7]
         ipAddress = data[2]
         mac = data[1]
         userName = data[3]
         apMacAddress = data[13]
         acLabel = data[14]
         ssid = data[5]       
         print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (upTime,apLabel,signalStrength,ipAddress,mac,userName,acLabel,ssid,apSwitchIp,apPort)
         count = count + 1
         data = []

#---------------------------------
#         Finish return
#---------------------------------------------------------------------------
print "</table>"
print "<FORM method='post' ACTION=\"./imc_rpt.py\">"
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



