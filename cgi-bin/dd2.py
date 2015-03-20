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
import json
import requests

#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
form = cgi.FieldStorage()
null = form.getvalue('null')
dest_ip = form.getvalue('dest_ip')
toe_ip = form.getvalue('toe_ip')
src_dpid = form.getvalue('src_dpid')
src_port = form.getvalue('src_port')
src_mac = form.getvalue('src_mac')
a_port = form.getvalue('a_port')
server = form.getvalue('server')
user = form.getvalue('user')
passw = form.getvalue('passw')


#Create authorization Token
auth = flare.XAuthToken(user=user,password=passw,controller=server)
my_flare=flare.Api(controller=server,auth=auth)


#----------------------------------------------------------------------------------------------------
#          Get the output port for the conversation
#----------------------------------------------------------------------------------------------------
flows = my_flare.get_flows(src_dpid)
	
for f in flows:
	if (f.match.eth_src == src_mac):
		out_port = f.actions.output
		
if (int(out_port) == int(a_port)):
	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title> FloTapr</title>"
	print "</head>"
	print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
	print "<FORM method='post' ACTION=\"./dd3.py\">"
	print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
	print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
	print "<HR> "
	print "<HR>"
	print "<textarea readonly name=\"instruct3\" cols=\"60\" rows=\"6\">The oringinal output port and analyzer port cannot \
	be the same use the Home button</textarea>"
	print "<HR>"
	print "<BR><BR>"
	print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
	print "<BR>"
	print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
	print "<BR>"
	print "<BR>"
	print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
	print "</body>"
	print "</html>"
	sys.exit()		
	
if (int(src_port) == int(a_port)):
	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title> FloTapr</title>"
	print "</head>"
	print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
	print "<FORM method='post' ACTION=\"./dd3.py\">"
	print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
	print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
	print "<HR> "
	print "<HR>"
	print "<textarea readonly name=\"instruct4\" cols=\"60\" rows=\"6\">The original source port and analyzer port cannot \
	be the same use the Home button</textarea>"
	print "<HR>"
	print "<BR><BR>"
	print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
	print "<BR>"
	print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
	print "<BR>"
	print "<BR>"
	print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
	print "</body>"
	print "</html>"
	sys.exit()			
	
	
out1 = "[{\"output\":%s},{\"output\":%s}]" % (out_port,a_port)
out2 = "[{\"output\":%s},{\"output\":%s}]" % (src_port,a_port)



flow1 = "{\"flow\": {\"priority\": 30000, \"idle_timeout\": 3000, \"match\": [{\"eth_type\": \"ipv4\"}, {\"ipv4_dst\": \"%s\"},\
{\"ipv4_src\": \"%s\"}], \"actions\": %s}}" % (dest_ip,toe_ip,out1)

flow2 = "{\"flow\": {\"priority\": 30000, \"idle_timeout\": 3000, \"match\": [{\"eth_type\": \"ipv4\"}, {\"ipv4_dst\": \"%s\"},\
{\"ipv4_src\": \"%s\"}], \"actions\": %s}}" % (toe_ip,dest_ip,out2)


url = "http://%s:8080/sdn/v2.0/of/datapaths/%s/flows" % (server,src_dpid)

r = requests.post(url, data=flow1,auth = auth, timeout=10)
if (r.status_code != 201):
	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title> FloTapr</title>"
	print "</head>"
	print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
	print "<FORM method='post' ACTION=\"./dd3.py\">"
	print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
	print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
	print "<HR> "
	print "<HR>"
	print "<textarea readonly name=\"instruct5\" cols=\"60\" rows=\"6\">Danger Will Robinson....The first flow was not set up propely \
	flow equals ..%s   return code %s</textarea>" % (flow1,r.status_code)
	print "<HR>"
	print "<BR><BR>"
	print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
	print "<BR>"
	print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
	print "<BR>"
	print "<BR>"
	print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
	print "</body>"
	print "</html>"
	sys.exit()
	
r = requests.post(url, data=flow2,auth = auth, timeout=10)
if (r.status_code != 201):
	print "Content-type:text/html\r\n\r\n"
	print "<html>"
	print "<head>"
	print "<title> FloTapr</title>"
	print "</head>"
	print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
	print "<FORM method='post' ACTION=\"./dd3.py\">"
	print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
	print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
	print "<HR> "
	print "<HR>"
	print "<textarea readonly name=\"instruct\" cols=\"60\" rows=\"6\">Danger Will Robinson....The second flow was not set up propely</textarea>"
	print "<HR>"
	print "<BR><BR>"
	print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
	print "<BR>"
	print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
	print "<BR>"
	print "<BR>"
	print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
	print "</body>"
	print "</html>"
	sys.exit()
#----------------------------------------------------------------------------------------------------
#          Create Dynamic Web Page
#----------------------------------------------------------------------------------------------------

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> FloTapr</title>"
print "</head>"
print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
print "<FORM method='post' ACTION=\"./dd3.py\">"
print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
print "<HR> "
print "<p>FloTapr has created the necessary flows. Verify the Analyzer is plugged into port %s on DPID:%s" % (a_port,src_dpid)
print "<br>"
print "<HR>"
print "<textarea readonly name=\"instruct\" cols=\"60\" rows=\"6\">The source flow from %s on port %s has been modified to have two output ports. \
The orginal port %s and the Analyzer port number %s</textarea>" % (toe_ip,src_port,out_port,a_port)
print "<BR>These are the processed flows sent to dpid %s" % (src_dpid)
print "<br><br><textarea readonly name=\"instruct1\" cols=\"60\" rows=\"6\">The FLOWS are...FLOW1 %s FLOW2 %s</textarea>" % (flow1,flow2)
print "<HR>"
print "<BR><BR>"
#print "These are the vars: %s, %s, %s, %s, %s, %s, %s, %s" % (conv,toe_ip,src_port,src_mac,user,passw,server,out_port)
print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>" 
print "<BR>"
print "<BR>"
print "<BR>"
print "<BR>" 
print "<BR>"
print "<BR>"  
print "<BR>"
print "<BR>"
print "<input type=\"hidden\" name=\"src_dpid\" value=%s>" % (src_dpid)
print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
print "<input type=\"hidden\" name=\"src_mac\" value=%s>" % (src_mac)
print " <center><input type=\"submit\" style=\"font-face: 'Comic Sans MS'; font-size: larger; color: black; background-color: #FF0000; border: 3pt ridge lightgrey\" value=\" Verify Flows\"></center>"
print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
print "<BR>"
print "<BR>"
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"


