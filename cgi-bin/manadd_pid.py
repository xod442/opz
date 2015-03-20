#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    manadd_pid.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#      added a if statement to check if the user wants to use glarn with IMC or not..Removing the IMC force use. 09/30/2014
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

# Check to see if anything was chozen. If pid_list is None goto Nothing Selected page and exit


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

# Set script variables
x = len(pid_list) 			# Keep track of how many items we need to process
c = 0 					# Basic counter
sel = 0                                 # Used to select all records in the glarn db
h_url =  "http://"                      # Prefix for URL
t_url = "/imcrs/plat/res/device?ip="    # Append to url
j = 0					# Switch for process IMC vs. Non-IMC entries
count = 0                               #  Another counter
#------------------------------------------------------------------------------
#          Mount the database
#-----------------------------------------------------------------------------
glarn = sqlite3.connect('/var/www/html/glarn.db')
gcur = glarn.cursor()



# put the list of selected dpids in the chozr table
print "Content-type:text/html\r\n\r\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<title> Wookieware.com</title>"
print "<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>"
print "<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>"
print "</head>"
#print "x is %s" % (x)
if x == 23:  # Only a single mac in the pid_list
    gcur.execute("SELECT * FROM chozr WHERE dpid ='%s'" % pid_list)
    row = gcur.fetchone()
    dpid = row[0]
    devip = row[1]
    mac = row[2]
    vendor = row[3]
    proc = 0
#------------------------------------------------------------------------- 
    if (imc != "on"):
     # Auth for imc
      auth=HTTPDigestAuth(imc_user,imc_passw)
      #	Prep the IP for API use and build API url
      api_url = "%s%s%s%s" % (h_url, imc_server, t_url, devip)
        # Now HTTP get to IMC for the device information...if it's there
      r = requests.get(api_url, auth=auth)
      if r.status_code == 200:

        #   Collect entries and write them to the dpid table in the glarn db
        #print "Lookiong in IMC...."
        tree = xml.fromstring(r.content)
        for node in tree.iter():
	    if (node.tag == 'label'):
	      sysName = node.text
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
    
      if 'contact' in locals():
        	#print "Right now contact is set to:%s" % (contact)
	  c = c + 1
	  j = 1
	  #  Write compete entry to glarn db	    
	  gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
	  glarn.commit()
	  #print "imc -1"
	  del contact
      elif j == 0:
         count = count + 1
         sysName = "None"
         contact = "None"
         location = "None"
         devid = 0
         gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
         glarn.commit()
        # print "no -IMC 1"
   
         del contact
    # IMC not being used
    else: 
       count = count + 1
       sysName = "None"
       contact = "None"
       location = "None"
       devid = 0
       gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
       glarn.commit()
elif j == 0:
  for i in pid_list:
    #print "At this point I equals %s" % (i)
    j = 0               # when j equal szero, it means we have not found an IMC entry. If IMC then set j to one.
    gcur.execute("SELECT * FROM chozr WHERE dpid ='%s'" % i)
    row = gcur.fetchone()
    dpid = row[0]
    devip = row[1]
    mac = row[2]
    vendor = row[3]
    proc = 0
#------------------------------------------------------------------------- 
# Auth for imc_passw
    if (imc != "on"):
      auth=HTTPDigestAuth(imc_user,imc_passw)
    #   	Prep the MAC for API use and build API url
      api_url = "%s%s%s%s" % (h_url, imc_server, t_url, devip)
      # Now HTTP get to IMC for the device information...if it's there
      r = requests.get(api_url, auth=auth)
      if r.status_code == 200:
       # print "Seraching IMC MUltiple loop...status conde:%s.." % (r.status_code)

        #   Collect entries and write them to the dpid table in the glarn db

        tree = xml.fromstring(r.content)
        for node in tree.iter():
	    if (node.tag == 'label'):
	      sysName = node.text
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
    
      if 'contact' in locals():
	  #print "Multiple loop contact is currently %s" % (contact)
	  c = c + 1
	  j = 1
	  #  Write compete entry to glarn db	    
	  gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
	  glarn.commit()
	  del contact   # Were using contact to see if we get results form IMC. This resets it for the next loop
	  #print "-IMC multiple write....."
      elif j == 0:
         count = count + 1
         sysName = "None"
         contact = "None"
         location = "None"
         devid = 0
         gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
         glarn.commit()
     #  print "NoIMC multiple write........"
         del contact
    # IMC not being used
    else: 
      count = count + 1
      sysName = "None"
      contact = "None"
      location = "None"
      devid = 0
      gcur.execute("INSERT into dpid VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",(dpid, mac, devip, sysName, contact, location, devid, vendor, sel))
      glarn.commit()
#--------------------------------------------------------------------------
#         Finish manual or go home
#---------------------------------------------------------------------------

print "<body>"
print "<h1> <img src=\"../../images/glarn.png\" width=\"50\" height=\"50\">glarn: The dpid database</h1>" 
print "<HR> "
print "<h3> Finished processing records</h3>"
print "<p>glarn has automatically added %s record(s) that it found in IMC, Additional records not found in IMC have been added with NULL fields." % (c)
print "There was a total of %s record(s) processed with NULL, use the edit dpid function to change entries</p>" % (count)
print "<FORM method='post' ACTION=\"./pid_main.py\">"
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

