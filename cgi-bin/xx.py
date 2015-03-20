#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    flo2_pid_pid.py
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
#  List flows from dpid
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


#------------------------------------------------------------------------------
#          Connect to the databases. These files must exists in /usr/lib/cgi-bin
#-----------------------------------------------------------------------------

glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()
gcur.execute('drop table if exists chozr')
gcur.execute('create table chozr (dpid text primary key, devip text, mac text, vendor text, proc int)')
glarn.commit()


#Create authorization Token for the SDN controller

auth = hp.XAuthToken(user=user,password=passw,server=server)
api=hp.Api(controller=server,auth=auth)

#Get dpid information from controller
dpidz = api.get_datapaths()
#--------------------------------------------------------------------------
# dpid factory: Break up dpis and match to vendor to determin MAC address
#---------------------------------------------------------------------------
# pad string
p = ":"
#Proc variable is used to tell if noimc db entries have been processed
proc = 0
for d in dpidz:
  pid = d.dpid.split(":")
  com_chk = pid[0]+p+pid[1]+p+pid[2]  #Comware dpid has oui as the first six bytes
  pro_chk = pid[2]+p+pid[3]+p+pid[4]  #Procurve dipd has oui starting on 3rd byte
  pro_chk = pro_chk.upper()
  com_chk = com_chk.upper()
  
#  Look in the oui database and see what matches we get  

  for row in ocur.execute("SELECT * FROM ouix WHERE oui ='%s'" % com_chk):
    vendor = row[1]
    mac = pid[0]+p+pid[1]+p+pid[2]+p+pid[3]+p+pid[4]+p+pid[5]
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

#          load entries into the noimc table (glarn db table noimc)

  gcur.execute("INSERT INTO chozr VALUES (?, ?, ?, ?, ?);", (d.dpid, d.device_ip, mac, vendor, proc))
  glarn.commit()
  
  #          now check to see if dpid lives in glarn db, if so delete it from noimc table

  for row in gcur.execute("SELECT * FROM dpid WHERE dpid ='%s'" % d.dpid):
    gcur.execute("DELETE FROM chozr WHERE dpid ='%s'" % d.dpid)
    glarn.commit()
    
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
print "<FORM method='post' ACTION=\"./manadd_pid.py\">"
print "<h1> <img src=\"../../images/glarn.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
print "<HR> "
print "<h3> This is a list of the dpids that are NOT in glarn<br>"
print "<select name=\"list_o_pids\" multiple=\"multiple\" size=\"10\">"
for row in gcur.execute("SELECT * FROM chozr WHERE proc=0"):
   dpid = row[0]
   print "<option value = \"%s\"> %s </option>" % (dpid,dpid)
print "</select>"
print "<br>"
print "Hold down the CTRL (windows) or the Command (Mac) key and select multiple dpids for processing<br>"
#print "<h3>%s record(s) have been automatically written to the glarn database...information was retrieved from IMC</h3>" % (c)
print "<input type=\"submit\" style=\"font-face: 'Arial'; font-size: larger; color: black; background-color: #0066FF; border: 3pt ridge lightgrey\" value=\" Add dpid\">"
print "</td>"
print "</tr>"
print "</table>"
print "<hr>"
#print " Vars %s, %s, %s, %s, %s, %s, %s, %s" % (dpid, mac, devip, sysName, contact, location, devid, vendor)
print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
print "<input type=\"hidden\" name=\"imc_server\" value=%s>" % (imc_server)
print "<input type=\"hidden\" name=\"imc_user\" value=%s>" % (imc_user)
print "<input type=\"hidden\" name=\"imc_passw\" value=%s>" % (imc_passw)
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"


