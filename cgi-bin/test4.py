#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    manadd2_pid.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#      Process manual entries
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
devid = form.getvalue('devid')
 
 
print "Devid %s" % (devid)


#------------------------------------------------------------------------------
#          Create database and tables
#-----------------------------------------------------------------------------
glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()
print "Counting rows"
# get total rows in database
gcur.execute("SELECT COUNT(*) FROM chozr")
count = gcur.fetchall()
totalRows = count[0][0]
print " Total rows in noimc database %s" % (totalRows)

if totalRows == 0:
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
  print "<h3> Finished adding manual entries. Return to the main menu</h3>" 
  print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
  print "<footer>"
  print "<a href=\"/index.html\">BACK</a>"
  print "<center><font face=\"Arial\" size=\"1\">SDN Solutions from WookieWare 2014</font></center>"
  print "<img src=\"../../images/wookieware.JPG\" width=\"50\" height=\"50\">"
  print "</footer>"
  print "</body>"
  print "</html>"
  glarn.close()
  sys.exit()
    # Get the first record to process

print "skip zero records for loop"
for row in gcur.execute("SELECT * FROM chozr WHERE proc=0"):
  dpid = row[0]
  mac = row[1]
  vendor = row[2]
  # This device is not im IMC set the devid to zero
  devid = 0
  # Now delete record after we extracted our variables
  #gcur.execute("DELETE FROM chozr WHERE dpid ='%s'" % dpid)
  #glarn.commit()
  print "--%s --%s  --%s" % (dpid, mac, vendor)
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
  print "<FORM method='post' ACTION=\"./man_add.py\">"
  print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Add Manual\">"
  print "</form>"
  print "<FORM method='post' ACTION=\"./pid_main.py\">"
  print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Home\"></center>"
  print "</form>"
  print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
  print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
  print "</body>"
  print "</html>"
  sys.exit()

