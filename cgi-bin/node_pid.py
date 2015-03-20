#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                   node_pid.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Pulls VARS from webform. 
#  Lists all nodes on a given controller
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




#Create authorization Token for the SDN controller

auth = hp.XAuthToken(user=user,password=passw,server=server)
api=hp.Api(controller=server,auth=auth)


#--------------------------------------------------------------------------
# dpid factory: Break up dpis and match to vendor to determin MAC address
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
print "<h3> All System Nodes</h3>"
print "<p>List of current nodes seen by the SDN controller"
print "<FORM method='post' ACTION=\"./pid_main.py\">"
nodesx = api.get_nodes()
print "<h1>All Nodes</h1>" 
print "<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">"
print "<tr><td>IP</td><td>MAC</td><td>VID</td><td>DPID</td><td>PORT</td> </tr>"
for n in nodesx:
  print "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (n.ip, n.mac, n.vid, n.dpid, n.port)
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






sys.exit()

