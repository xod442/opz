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
#import cgitb; cgitb.enable()
import hpsdnclient as hp
import sqlite3
import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as xml

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------


server = "10.132.0.102"
user = "sdn"
passw = "skyline"
imc_server = "10.132.0.106:8080"
imc_user = "admin"
imc_passw = "admin"


#------------------------------------------------------------------------------
#          Connect to the databases. These files must exists in /usr/lib/cgi-bin
#-----------------------------------------------------------------------------
print "connecting to databases....."
oui = sqlite3.connect('/var/www/html/oui.db')
ocur = oui.cursor()

glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()

#Create authorization Token for the SDN controller

auth = hp.XAuthToken(user=user,password=passw,server=server)
api=hp.Api(controller=server,auth=auth)

#Get dpid information from controller
print "Sending SDN API now...."
dpidz = api.get_datapaths()
#--------------------------------------------------------------------------
# dpid factory: Break up dpis and match to vendor to determin MAC address
#---------------------------------------------------------------------------
# pad string
p = ":"
#Proc variable is used to tell if noimc db entries have been processed
proc = 0
print "++++++++++++++++++++Begin Processing +++++++++++++++++++++++++++++++"
for d in dpidz:
  pid = d.dpid.split(":")
  print "This is d.dpid var %s" % (d.dpid)
  com_chk = pid[0]+p+pid[1]+p+pid[2]  #Comware dpid has oui as the first six bytes
  pro_chk = pid[2]+p+pid[3]+p+pid[4]  #Procurve dipd has oui starting on 3rd byte
  com_chk = com_chk.upper()
  pro_chk = pro_chk.upper()
  print "this is com_chk var %s" % (com_chk)
  print "this is pro_chk var %s" % (pro_chk)
#  Look in the oui database and see what matches we get  
  print "Checking for comware oui "
  for row in ocur.execute("SELECT * FROM ouix WHERE oui ='%s'" % com_chk):
    vendor = row[1]
    mac = pid[0]+p+pid[1]+p+pid[2]+p+pid[3]+p+pid[4]+p+pid[5]
  print "Checking the procurve oui"
  for row in ocur.execute("SELECT * FROM ouix WHERE oui ='%s'" % pro_chk):
    vendor = row[1]
    mac = pid[2]+p+pid[3]+p+pid[4]+p+pid[5]+p+pid[6]+p+pid[7]

#    If the test is all zeros then it is most likely mininet dpid

  if com_chk == "00:00:00":
    vendor = "unknown"
    mac = pid[2]+p+pid[3]+p+pid[4]+p+pid[5]+p+pid[6]+p+pid[7]
  if pro_chk == "00:00:00":
    vendor = "unknown"
    mac = pid[2]+p+pid[3]+p+pid[4]+p+pid[5]+p+pid[6]+p+pid[7]
  print " This is the mac var %s" % (mac)
  print " This is the vendor var %s" % (vendor)
  print " This is the dpid var %s" % (d.dpid)
  print " This is the proc var %s" % (proc)
#          load entries into the noimc table (glarn db table noimc)

  print "Writing entries to noimc table"
  glarn.execute("INSERT INTO noimc VALUES (?, ?, ?, ?);", (d.dpid, mac, vendor, proc))
  glarn.commit()
  print "-------------------------------------------------------------------"
  #          now check to see if dpid lives in glarn db, if so delete it from noimc table

  for row in gcur.execute("SELECT * FROM dpid WHERE dpid ='%s'" % d.dpid):
    glarn.execute("DELETE FROM noimc WHERE dpid ='%s'" % d.dpid)
    glarn.commit()
    
#--------------------------------------------------------------------------
#          IMC factory: Now take the remaining entries in the noimc table
#          and use the eAPI to find addition information about the dpid
#          populate glarn with the added info.
#
#          The remaining entries will be sent to the entry form loader
#          where the additional infor will be manually entered.
#------------------------------------------------------------------------- 
"""
# Auth for imc_passw

auth=HTTPDigestAuth(imc_user,imc_passw)

   
h_url =  "http://"
t_url = "/imcrs/plat/res/device?mac="
c = 0
for row in gcur.execute("SELECT * FROM noimc WHERE proc=0"):
   dpid = row[0]
   mac = row[1]
   vendor = row[2]
   proc = row[3]
   
   #	Prep the MAC for API use and build API url
      
   xmac = mac.replace(":", "%3A")
   api_url = "%s%s%s%s" % (h_url, imc_server, t_url, xmac)

  # Now HTTP get to IMC for the device information
   
   r = requests.get(api_url, auth=auth)
   if r.status_code == 200:

  #   Collect entries and write them to the dpid table in the glarn db

	tree = xml.fromstring(r.content)
	for node in tree.iter():
		if (node.tag == 'label'):
			sysName = node.text
	for node in tree.iter():
		if (node.tag == 'ip'):
			devip = node.text
	for node in tree.iter():
		if (node.tag == 'contact'):
			contact = node.text		
	for node in tree.iter():
		if (node.tag == 'location'):
			location = node.text
	for node in tree.iter():
		if (node.tag == 'id'):
			devid = node.text
#
#
#    At this point we know the return from IMC was good. Check to see if we have valid information
#    If so, then go ahead and process db.
#
	if 'devip' in locals():
	    c = c + 1		    
	# Delete the noimc record so all that is left in the table are manual entries
			
	    glarn.execute("DELETE FROM noimc WHERE dpid ='%s'" % dpid)
	    glarn.commit()

	#  Write compete entry to glarn db
	
	    glarn.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor))
	    glarn.commit()
            print " Vars %s, %s, %s, %s, %s, %s, %s, %s" % (dpid, mac, devip, sysName, contact, location, devid, vendor)


"""