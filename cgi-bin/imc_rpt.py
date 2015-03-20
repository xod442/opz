#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    imc_rpt.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Pulls VARS from webform. 
#  launches different reports
#
#------Might not need this but please they are handy------------------------ 
#
# Do the imports!!!! 
#----------------------If you dont have it use "apt-get install (name)"

import sys 
import subprocess
import cgi
import cgitb; cgitb.enable()
import sqlite3

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------

form = cgi.FieldStorage()

imc_server = form.getvalue('imc_server')
imc_user = form.getvalue('imc_user')
imc_passw = form.getvalue('imc_passw')


if imc_server is None:
  print "Content-type:text/html\r\n\r\n"
  print "<!DOCTYPE html>"
  print "<html>"
  print "<head>"
  print "<title> Wookieware.com</title>"
  print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
  print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
  print "</head>"
  print "<body>"
  print "<h1> <img src=\"../../images/report.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
  print "<h3>No IP address for the IMC server</h3>"
  print "<p>You did not enter the IP address of the IMC Server, go back to the begining and enter the IP address.</p>"
  print "<HR> "
  print "<a href=\"/index.html\">BACK</a>"  
  sys.exit()
if imc_user is None:
  print "Content-type:text/html\r\n\r\n"
  print "<!DOCTYPE html>"
  print "<html>"
  print "<head>"
  print "<title> Wookieware.com</title>"
  print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
  print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
  print "</head>"
  print "<body>"
  print "<h1> <img src=\"../../images/report.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
  print "<h3>No username for the IMC user</h3>"
  print "<p>You did not enter the IP username, go back to the begining and enter the missing information.</p>"
  print "<HR> "
  print "<a href=\"/index.html\">BACK</a>"  
  sys.exit()
if imc_passw is None:
  print "Content-type:text/html\r\n\r\n"
  print "<!DOCTYPE html>"
  print "<html>"
  print "<head>"
  print "<title> Wookieware.com</title>"
  print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
  print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
  print "</head>"
  print "<body>"
  print "<h1> <img src=\"../../images/report.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
  print "<h3>No Password for the SDN controller</h3>"
  print "<p>You did not enter the password for the SDN controller go back to the begining and enter the missing information.</p>"
  print "<HR> "
  print "<a href=\"/index.html\">BACK</a>"  
  sys.exit()
#------------------------------------------------------------------------------
#          Create database and tables
#-----------------------------------------------------------------------------
#db = sqlite3.connect('/usr/lib/cgi-bin/oui.db')
#cur = db.cursor()

#Create authorization Token

#auth = hp.XAuthToken(user=user,password=passw,server=server)
#api=hp.Api(controller=server,auth=auth)

#Get information from controller
#dpidz = api.get_datapaths()

#-----------------------------------------------------------------------------
#          Create Dynamic Web Page
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
print "<h1> <img src=\"../../images/report.png\" width=\"125\" height=\"60\">   IMC API reporting</h1>" 
print "<h3>Main Selections</h3>"
print "<p>Choose from one of the selections below. Each button will launch a different report."
print "<HR> "
#print " --server %s, --user %s, --passw %s, --imc_server %s, --imc_user %s, --imc_passw %s" % (server, user, passw, imc_server, imc_user, imc_passw)
print "<table>"
print "<tr>"
print "<td>"
print "<FORM method='post' ACTION=\"./imc_dev.py\">"
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Device Inventory\"></center>"
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "</form>"
print "</td>"
print "</tr>"
print "<tr>"
print "<td>"
print "<FORM method='post' ACTION=\"./wireless_client1.py\">"
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" User Experience\"></center>"
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "</form>"
print "</td>"
print "</tr>"
print "</table>"
print "<hr>"
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"
print "<footer>"
print "<center><font face=\"Arial\" size=\"1\">IMC Solutions from WookieWare 2014</font></center>"
print "<img src=\"../../images/wookieware.JPG\" width=\"50\" height=\"50\">"
print "<a href=\"/index.html\">BACK</a>" 
print "</footer>"
print "</body>"
print "</html>"


