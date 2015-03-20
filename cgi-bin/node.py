#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    "node.py"
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....
#
#
##--------------------------------------------------------------------------
#  Initial release - Pulls VARS from webform. 
#  completes several tasks.
#
#------Might not need this but please they are handy------------------------ 
#
# Do the imports!!!! 
#----------------------If you dont have it use "apt-get install (name)"
import cgi
import cgitb; cgitb.enable() 
import hpsdnclient as hp
#-------------------------------------------------------------------------
#   Uncomment the next line to turn on python debugging
#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
form = cgi.FieldStorage()
server = form.getvalue('server')
user = form.getvalue('user')
passw = form.getvalue('passw')
#
#
i  #
# Create an auth token for SDN controller:
auth = hp.XAuthToken(user=user,password=passw,server=server)
api=hp.Api(controller=server,auth=auth)
#
#
#----------------------------------------------------------------------------------------------------
#          Create Dynamic Web Page
#----------------------------------------------------------------------------------------------------

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<!-- This is a comment -->"
print "<title> Your Results</title>"
print "</head>"
print "<body>"
print "<FORM method='post' ACTION=\"./iLOLD.py\">"
#
#
#Get information from controller (HTTP GET)
nodesx=api.get_nodes()
for n in nodesx:
    print "--%s, --%s, --%s, --%s, --%s" % (n.ip, n.mac, n.vid, n.dpid, n.port)
    print "<br>"
#
#
#
print "<hr> "
print "<p>Thank you for taking the time to use this script</p>"
print "<br>"
print "<HR>"
print "<p>For more information on how to use this application <a href=\"/faq.html\">User Guide</a></p>"  
print "<a href=\"/index.html\">Home</a>"
print "<br>"
print "<br>"
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"

