#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    flotapr -dd2.py
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
import sys 
import subprocess
import cgi
import cgitb; cgitb.enable()
import hpsdnclient as flare
import sqlite3

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
form = cgi.FieldStorage()
null = form.getvalue('null')
src_dpid = form.getvalue('src_dpid')
server = form.getvalue('server')
user = form.getvalue('user')
passw = form.getvalue('passw')
src_mac = form.getvalue('src_mac')


#Create authorization Token
auth = flare.XAuthToken(user=user,password=passw,controller=server)
my_flare=flare.Api(controller=server,auth=auth)

#Get information from controller
#nodesx = my_flare.get_nodes()


#----------------------------------------------------------------------------------------------------
#          Get the flows from the dpid
#----------------------------------------------------------------------------------------------------
flows = my_flare.get_flows(src_dpid)
#----------------------------------------------------------------------------------------------------
#          Create Dynamic Web Page
#----------------------------------------------------------------------------------------------------

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> FloTapr</title>"
print "</head>"
print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
print "<FORM method='post' ACTION=\"./cgi-bin/ddx.py\">"
print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
print "<HR> "
print "<p>FloTapr has analyzed the current flows for dpid %s" % (src_dpid)
print "<br>"
print "<HR>"
for f in flows:
	eth_src = f.match.eth_src
	eth_dst = f.match.eth_dst
	#ip_src = f.match.ipv4_src
	#ip_dst = f.match.ipv4_dst
	action = f.actions.output
	if (eth_src == src_mac):
		print "<p>Host MAC %s has a flow to destination MAC %s on port(s) %s" % (eth_src,eth_dst,action)
print "<HR>"
print "<BR>"
print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
print "<BR>"
print "<BR>"
print "<BR>"
print "<BR>" 
print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
print "<BR>"
print "<BR>"
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"


