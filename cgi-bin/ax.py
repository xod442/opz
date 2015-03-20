#!/usr/bin/env python

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml
from xml.etree.ElementTree import Element, SubElement, tostring
#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
def main():
  
  #Change these to your credentials
   
  imc_server = "10.132.0.108:8080"
  imc_user = "admin"
  imc_passw = "admin"
 
  #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  STOP EDITING  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

  # Set script variables
  data = []
  h_url =  "http://"                      		# Prefix for URL
  
  #
  #    Change the size value to match you number of access points ((((Set to 1 by default))))))!!!!!!!!!!!!
  #
  #
  #--------------------------------V
  t_url = "/imcrs/plat/res/device?size=1&category=9"    	# Append to url set size for amount of devices to pull 5K will get all category 9 (Desktops)
  c_url = "/imcrs/plat/res/device/"			# Change URL begining
  fin_url = "/updateCategory"                           # Finish URL
  count = 0  
  new_id = str(5)

  # Create command XML string c info for changing the categoryId field
  root = Element('device')
  child = SubElement(root, "categoryId")
  child.text = "5"
  c_info = tostring(root)
  
  headers = {'Accept': 'application/xml','Content-Type': 'application/xml; charset=utf-8', 'Accept-encoding': 'application/xml', 'Connection': 'Keep-Alive'}

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
           # Create the URL for the HTTP PUT
           api_url = "%s%s%s%s%s" % (h_url, imc_server, c_url, idx, fin_url)

          # Now send the command this is an HTTP PUT
           
	   r = requests.put(api_url, data=c_info, auth=auth, headers=headers)
	   
	   if r.status_code == 204:
	      # Update user if change was successful
	      count = count + 1
	      print "Device ID "+idx+" was changed from desktop to wireless" 
              	         
           data = []          
  print "total records processed %s" % (count)
if __name__ == '__main__':
  main()




