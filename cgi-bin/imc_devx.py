#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    imc_devx.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#      IFnd devices discovered as desktop and change to wireless
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
import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml
from xml.etree.ElementTree import Element, SubElement, tostring
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
  

  # Set script variables
  data = []
  h_url =  "http://"                      		# Prefix for URL
  t_url = "/imcrs/plat/res/device?size=5000&category=9"    	# Append to url set size for amount of devices to pull 5K will get all category 9 (Desktops)
  c_url = "/imcrs/plat/res/device/"			# Change URL begining
  fin_url = "/updateCategory"                           # Finish URL
  count = 0  
  new_id = str(5)

  # Create command XML string c info for changing the categoryId field
  root = Element('device')
  child = SubElement(root, "categoryId")
  child.text = "5"
  c_info = tostring(root)




                             		#  Another counter

  ts = int(time.time())
  ts = str(ts) 			#convert to string
  namex = "/var/www/Appolis"
  tail = ".txt"
  filex = namex+ts+tail		#to save configuration changes with unique filename
  cr= "\n"
  #	Open file for writing script progress
  
  open(filex,'w').close()	# Touch file
  f = open(filex,'a+')
  banner = "=========================[[[Appolis processed entries]]]===================================="
  f.write(banner)
  f.write(cr)

  
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
  print "<h1> IMC API Device Name Change</h1>"
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
	   idx = data[1]
           
           api_url = "%s%s%s%s%s" % (h_url, imc_server, c_url, idx, fin_url)
             
           # Create command XML string c data for changing the categoryId field
           
           xxx = 'onceuponatimeigaveafuck'
           print "%s" % (xxx)
           #print "<br>"
          
          
          # Now send the command this is an HTTP PUT
           
	   r = requests.post(api_url, data=c_info, auth=auth, headers=headers)
	   if r.status_code == 200:
	      count = count + 1
	      line = "Device ID "+idx+" was changed from desktop to wireless" 
              f.write(line)
	      f.write(cr)
	         
           data = []          
#---------------------------------
#         Finish return page
#---------------------------------------------------------------------------
  print "<HR> "
  print "<h3> Total number of devices that changed category %s </h3>" % (count)
  print "This is the api_url %s" % (api_url)
  print "<br>"
  print "This is the c_info %s" % (c_info)
  print "<br>"
  print "This is the current device id %s" % (idx)
  print "<br>"
  print "This is the last r.status %s" % (r.status_code)
  print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Home\"></center>"
  print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
  print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
  print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
  print "</form>"
  print "<footer>" 
  print "<a href=\"/imc_devx.html\">BACK</a>" 
  print "<center><font face=\"Arial\" size=\"1\">IMC Solutions From WookieWare 2014</font></center>"
  print "</footer>"
  print "</body>"
  print "</html>"
  f.close()
if __name__ == '__main__':
  main()




