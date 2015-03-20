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
import time
import subprocess
import cgi
import cgitb; cgitb.enable()
import hpsdnclient as hp
import sqlite3
import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml
from netaddr import *
#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
def main():
  form = cgi.FieldStorage()
  imc_server = form.getvalue('imc_server')
  imc_user = form.getvalue('imc_user')
  imc_passw = form.getvalue('imc_passw')
  #dev_type = form.getvalue('dev_type')
  
  # Get the IP address range and conver to integers for comparison
  ipStart = form.getvalue('ipStart')
  ipStart = IPAddress(ipStart)
  ipStart = int(ipStart) 
  
  ipStop = form.getvalue('ipStop')
  ipStop = IPAddress(ipStop)
  ipStop = int(ipStop)
 

  # Set script variables
  data = []
  h_url =  "http://"                      	# Prefix for URL
  t_url = "/imcrs/plat/res/device?size=20000"    	# Append to url set size for amoutn of devices to pull 10K will gett all entries from most servers
  c_url = "/imcrs/icc/confFile/executeCmd"
  count = 0                               	#  Another counter

  ts = int(time.time())
  ts = str(ts) 			#convert to string
  namex = "/var/www/Appolis"
  tail = ".txt"
  filex = namex+ts+tail		#to save configuration changes with unique filename
  cr= "\n"
  #	Open file for writing script progress
  
  open(filex,'w').close()	# Touch file
  f = open(filex,'a+')
  banner = "=========================Appolis processed entries===================================="
  f.write(banner)
  f.write(cr)
  
  
  # what type of devices will be processed.
  dev_type = "switch"
 
  # Add additional MAC headers as necessary
  comware1 = "00:23:89"
  comware2 = "d0:7e:28"
  testMac = "00:00:00"
  
  headers = {'Accept': 'application/xml','Content-Type': 'application/xml; charset=utf-8', 'Accept-encoding': 'application/xml', 'Connection': 'Keep-Alive'}
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
  #print "<h1> <img src=\"../../images/report.png\" width=\"125\" height=\"60\">   IMC API reporting</h1>" 
  print "<h1> IMC API Command Delivery</h1>"
#------------------------------------------------------------------------- 

  #import pdb; pdb.set_trace()
  # Auth for imc
  auth=HTTPDigestAuth(imc_user,imc_passw)
  #	Prep the IP for API use and build API url
  api_url = "%s%s%s" % (h_url, imc_server, t_url)
  # Now HTTP get to IMC for the device information...if it's there
  r = requests.get(api_url, auth=auth)
  if r.status_code == 200:
    
     tree = xml.fromstring(r.content)
    
     for node in tree.iter():
    
       data.append(node.text)
     
       # If node.tag is the parent tag clear the data[] array and iterate
       if node.tag == 'list':
           data = []
   
       # If link then we have processed the full xml element for the current device
       if node.tag == 'link':
           ip = data[3]
           ipStr = data[3]
           ip = IPAddress(ip)
           ip = int(ip)
           
           if ip >= ipStart and ip <= ipStop:
	       print "IP address %s" % (ipStr)
	       print "<br>"
               nas = "nas-ip "
               commandx = nas+ipStr 
           
               typex = data[12]	   
               #print "%s" % (typex)
               idx = data[1]
               label = data[2]
               mask = data[4]
               status = data[6]
               sysName = data[7]
               contact = data[8]
               location = data[9]
               name = data[21]
               mac = data[22]
               if mac:
                 mac = mac.split(":")
                 testMac = mac[0]+":"+mac[1]+":"+mac[2]
           
           
           #---------------------------------------------------------------
           #   If we have a device type match, push the commands
           #---------------------------------------------------------------
           
           
               if typex == dev_type and testMac == comware1 or testMac == comware2:
	         print "Its a switch"
	         print "<br>"
                 count = count + 1
                 api_url = "%s%s%s" % (h_url, imc_server, c_url)
             
                 # Create command XML string c data for the command delivery and s_data for the save of the configuration
                 c_data = "<deviceExecuteCmd><deviceId>%s</deviceId><cmdlist><cmd>system-view</cmd><cmd>radius scheme wireless</cmd><cmd>%s</cmd><cmd>save</cmd><cmd>y</cmd><cmd>%s</cmd></cmdlist></deviceExecuteCmd>" % (idx,commandx,filex)
             
             
                 # Now send the command
           
	         r = requests.post(api_url, data=c_data, auth=auth, headers=headers)
	         line = "Device ID "+idx+" trying .... command is "+commandx 
	         f.write(line)
	         f.write(cr)
	         if r.status_code != 200:
	           pass
           data = []
        
           
           
           
           
           
#---------------------------------
#         Finish return
#---------------------------------------------------------------------------
  print "<HR> "
  print "<h3> Command delivered to %s %s </h3>" % (count,dev_type)
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
  f.close()
if __name__ == '__main__':
  main()




