#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    flo_pid.py
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
#  Calls glarn chooser and deletes selected entries
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
imc = form.getvalue('imc')

sel = 0 # allows for selecting all the records in glarn
#------------------------------------------------------------------------------
#          Connect to the database. ThIS files must exists in /var/www/html
#-----------------------------------------------------------------------------

glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()

    
#
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
print "<FORM method='post' ACTION=\"./flox_pid.py\">"
#print "<FORM method='post' ACTION=\"./flo2_pid.py\">"
print "<h1> <img src=\"../../images/glarn.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
print "<HR> "
print "<h3> This is a list of dpids in glarn. select the dpids to view their flows<br>"
print "<select name=\"list_o_pids\" multiple=\"multiple\" size=\"10\">"
for row in gcur.execute("SELECT * FROM dpid WHERE sel ='%s'" % sel):
   dpid = row[0]
   print "<option value = \"%s\"> %s </option>" % (dpid,dpid)
print "</select>"
print "<br>"
print "Hold down the CTRL (windows) or the Command (Mac) key and select multiple dpids for processing<br>"
#print "<h3>%s record(s) have been automatically written to the glarn database...information was retrieved from IMC</h3>" % (c)
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Dpid Flows\">"
print "<hr>"
print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "<input type=\"hidden\" name=\"imc\" value=%s>" % (imc)
print "</form>"
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
print "<footer>"
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions from WookieWare 2014</font></center>"
print "<img src=\"../../images/wookieware.JPG\" width=\"50\" height=\"50\">"
print "<a href=\"/index.html\">Home</a>" 
print "</footer>"
print "</body>"
print "</html>"


