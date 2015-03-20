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
#  build a database of all dpids not in glarn
#  Calls glarn chooser 
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
server = "10.132.0.102"
user = "sdn"
passw = "skyline"
imc_server = "10.132.0.106:8080"
imc_user = "admin"
imc_passw = "admin"
#------------------------------------------------------------------------------
#          Create database and tables
#-----------------------------------------------------------------------------
print "open db"

glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()

# drop table and clear it....make new



count = 1
line = 5


gcur = glarn.execute("SELECT * FROM chozr WHERE proc ='%s'" % 0)
x =  gcur.fetchall()
if line <= count: 

  print x[count]
  count = count + 1 
"""
if line <= count: 
  x =  gcur.fetchall()[count]
  dpid = x[0]
  mac = x[1]
  vendor = x[2]
  count = count + 1 
  print "vendor = %s, dpid = %s, mac = %s" % (vendor, dpid, mac)
glarn.close()

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
    t_url = "/imcrs/plat/res/device?mac="
    c = 0

    # Get entry from the chozr table

      
      #	Prep the MAC for API use and build API url
	  
    xmac = mac.replace(":", "%3A")
    api_url = "%s%s%s%s" % (h_url, imc_server, t_url, xmac)

      # Now HTTP get to IMC for the device information...if it's there
      
    r = requests.get(api_url, auth=auth)
    print r.status_code
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
                print "Found in IMC"
		c = c + 1		    
	    # Delete the noimc record so all that is left in the table are manual entries
			    
		gcur.execute("DELETE FROM noimc WHERE dpid ='%s'" % dpid)
		gcur.commit()

	    #  Write compete entry to glarn db
	        print "Writing to dpid datbase auto record"
		gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor))
		glarn.commit()
		##print " Vars %s, %s, %s, %s, %s, %s, %s, %s" % (dpid, mac, devip, sysName, contact, location, devid, vendor)

    #
#     Now glarn has entered all the records found in IMC automatically to the dpid database
#
#     The netx process presents the first manual entery screens
#     First let's check if there is anything to process
#

# get total rows in database
#gcur.execute("SELECT COUNT(*) FROM noimc")
#count = gcur.fetchall()
#totalRows = count[0][0]

#if totalRows > 0:
  
print " Getting first record from noimc db"
  # Get the first record to process
gcur.execute("SELECT * FROM noimc WHERE proc=0")
dpid = row[0]
mac = row[1]
vendor = row[2]
  # This device is not im IMC set the devid to zero
devid = 0
  # Now delete record after we extracted our variables
gcur.execute("DELETE FROM noimc WHERE dpid ='%s'" % dpid)
glarn.commit()  
#--------------------------------------------------------------------------
#         dpid chooser screen
#---------------------------------------------------------------------------
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title> Wookieware.com</title>"
print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
print "</head>"
print "<body>"
print "<h1> <img src=\"../../images/glarn.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
print "<HR> "
print "glarn has automatically added %s records that it found in IMC" % (c)
print "<FORM method='post' ACTION=\"./manadd2_pid.py\">"
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Add dpid\">"
print "<h3> Manual Entry</h3>"
print "<p> Fill out the empty fields and contnue</p>"
print "<hr>"
print "dpid: <input type \"text\" name =\"dpid\" value = %s>   mac address: <input name =\"mac\" value = %s><br> " % (dpid, mac)
print "vendor: <input name =\"vendor\" value = %s size=\"10\"><br>" % (vendor)
print "<hr>"
print "IP address: <input name =\"devip\" size=\"15\">   sysName: <input name =\"sysName\" size=\"15\"><br> "
print "Contact: <input name =\"contact\" size=\"15\">   location: <input name =\"location\" size=\"20\"><br> "
print "<input type=\"hidden\" name=\"devid\" value=%s>" % (devid)
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"
glarn.close()

"""
