#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    dpids
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Pulls VARS from webform. 
#  List datapath identifiers
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
mac = "0d:7e:28:80:41:8f"
#--------------------------------------------------------------------------
#          IMC factory: Now take the remaining entries in the noimc table
#          and use the eAPI to find addition information about the dpid
#          populate glarn with the added info.
#
#          The remaining entries will be sent to the entry form loader
#          where the additional infor will be manually entered.
#------------------------------------------------------------------------- 

# Auth for imc_passw

auth=HTTPDigestAuth(imc_user,imc_passw)

   
h_url =  "http://"
t_url = "/imcrs/plat/res/device?size=1000"
label = "Not Defined"
sysName = "Not Defined"
contact = "Not Defined"
location = "Not Defined"
devid = "Not Defined"
category = "Not Defined"
devip = "Not Defined"
mask = "Not Defined"
mac = "Not Defined"
  
   #	Prep the MAC for API use
      
#xmac = mac.replace(":", "%3A")
#xmac = "10.132.0.253" 
api_url = "%s%s%s" % (h_url, imc_server, t_url)

data = []
   
r = requests.get(api_url, auth=auth)

print r

tree = xml.fromstring(r.content)
t = len(tree)

for node in tree.iter():
  data.append(node.text)
  if node.tag == 'link':
    length = len(data)
    print length
    print "========================================================="
    print data 
    data = []
   
  #print "%s, %s" % (node.tag, node.text)
  
"""
  if (node.tag == 'list'):
      listx = node.text
  if (node.tag == 'device'):
      device = node.text		
  if (node.tag == 'label'):
      label = node.text      
  if (node.tag == 'status'):
      status = node.text
  if (node.tag == 'statusDesc'):
      stat_d = node.text
  if (node.tag == 'sysOid'):
      sysOid = node.text
  if (node.tag == 'sysDescription'):
      sysDesc = node.text
  if (node.tag == 'topoIconName'):
      icon = node.text
  if (node.tag == 'categoryID'):
      catId = node.text
  if (node.tag == 'symbolId'):
      sId = node.text		
  if (node.tag == 'symbolType'):
      sType = node.text      
  if (node.tag == 'symbolName'):
      sName = node.text
  if (node.tag == 'symbolDesc'):
      sDesc_d = node.text
  if (node.tag == 'symbolLevel'):
      sLevel = node.text
  if (node.tag == 'parentId'):
      pId = node.text
  if (node.tag == 'typeName'):
      tName = node.text
  if (node.tag == 'link'):
      link = node.text
  if (node.tag == 'sysName'):
      sysName = node.text
  if (node.tag == 'contact'):
      contact = node.text		
  if (node.tag == 'location'):
      location = node.text      
  if (node.tag == 'id'):
      devid = node.text
  if (node.tag == 'devCategorgyImgSrc'):
      category = node.text
  if (node.tag == 'ip'):
      devip = node.text
  if (node.tag == 'mask'):
      mask = node.text
  if (node.tag == 'mac'):
      mac = node.text
print "%s, %s, %s ,%s, %s, %s, %s, %s, %s" % (label, sysName, contact, location, devid, category, devip, mask, mac)

for node in tree.iter():
  print "==================================="
  print "This is node tag %s" % (node.tag)
  print "This is node text %s" % (node.text)
print  api_url
#print mac
#print api_url
"""