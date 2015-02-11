#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    list2_pid.py
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
server = form.getvalue('server')
user = form.getvalue('user')
passw = form.getvalue('passw')
imc_server = form.getvalue('imc_server')
imc_user = form.getvalue('imc_user')
imc_passw = form.getvalue('imc_passw')
pid_list = form.getvalue('list_o_pids')
imc = form.getvalue('imc')

if pid_list == None:
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
  print "<h1> No items selected</h1>"
  print "<FORM method='post' ACTION=\"./pid_main.py\">"
  print "<h3> List is empty </h3>"
  print "<p> Click button below to go back to the system chooser</p>"
  print "<hr>"
  print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Main Menu\">"
  print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
  print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
  print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
  print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
  print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
  print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
  print "<input type=\"hidden\" name=\"imc\" value=%s>" % (imc)
  print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
  print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
  print "</body>"
  print "</html>"
  #glarn.close()
  sys.exit()

x = len(pid_list) # Keep track of how many items we need to process

c = 0
sel = 0
j = 0

#------------------------------------------------------------------------------
#          Create database and tables
#-----------------------------------------------------------------------------
glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()
gcur2 = glarn.cursor()


  

# Check to see if anything was chozen. If x is zero goto Nothing Selected page and exit






  

#--------------------------------------------------------------------------
#         Finish manual or go home
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
print "<h3> List of dpids</h3>"
print "<p>This is the list of dpids that were selected"
print "<FORM method='post' ACTION=\"./pid_main.py\">"
print "<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">"
print "<tr>"
print "<td>dpid</td>" 
print "<td>mac</td>"  
print "<td>devip</td>" 
print "<td>sysName</td>" 
print "<td>contact</td>"  
print "<td>location</td>"  
print "<td>devid</td>"  
print "<td>vendor</td>" 
print "</tr>"


if x == 23:      #only one entry (dpids are 23 chars long
  j = 1
  for row in gcur.execute("SELECT * FROM dpid WHERE dpid ='%s'" % pid_list):
    dpid = row[0]
    mac = row[1]
    devip = row[2]
    sysName = row[3]
    contact = row[4]
    location = row[5]
    devid = row[6]
    vendor = row[7]
    print "<tr>"
    print "<td>%s</td>" % (dpid)
    print "<td>%s</td>" % (mac)
    print "<td>%s</td>" % (devip)
    print "<td>%s</td>" % (sysName)
    print "<td>%s</td>" % (contact)
    print "<td>%s</td>" % (location)
    print "<td>%s</td>" % (devid)
    print "<td>%s</td>" % (vendor)
    print "</tr>"
    break   # get out after one...I'm tired fighting this
elif j == 0:
    for i in pid_list:
      for row in gcur.execute("SELECT * FROM dpid WHERE dpid ='%s'" % i):
	dpid = row[0]
	mac = row[1]
	devip = row[2]
	sysName = row[3]
	contact = row[4]
	location = row[5]
	devid = row[6]
	vendor = row[7]
	print "<tr>"
	print "<td>%s</td>" % (dpid)
	print "<td>%s</td>" % (mac)
	print "<td>%s</td>" % (devip)
	print "<td>%s</td>" % (sysName)
	print "<td>%s</td>" % (contact)
	print "<td>%s</td>" % (location)
	print "<td>%s</td>" % (devid)
	print "<td>%s</td>" % (vendor)
	print "</tr>"
print "</table>"
print "<HR>"
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Main Menu\">"
print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "<input type=\"hidden\" name=\"imc\" value=%s>" % (imc)
print "</form>"
print "<footer>"
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
print "<a href=\"/index.html\">BACK</a>" 
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</footer>"
print "</body>"
print "</html>"






glarn.close()
sys.exit()

