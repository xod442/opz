#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    flotapr
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

"""
print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> FloTapr</title>"
print "</head>"
print "<body background=\"/wookie_tap_back.GIF\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
print "<center><img border=\"0\" src=\"/flowtapper.png\" width=\"300\" height=\"75\"></center>"
print "<center><H1> Processing Please Standby!</H1></center>" 
print "<HR> "

"""
#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
form = cgi.FieldStorage()
null = form.getvalue('null')
server = form.getvalue('server')
user = form.getvalue('user')
passw = form.getvalue('passw')
toe_ip = form.getvalue('toe_ip')
a_port = form.getvalue('a_port')
#----------------------------------------------------------------------------------------------------
#          Create database and tables
#----------------------------------------------------------------------------------------------------
#db = sqlite3.connect('database.db')
db = sqlite3.connect(':memory:')
db.execute('drop table if exists nodes')
db.execute('drop table if exists flows')
db.execute('drop table if exists conv')
db.execute('create table nodes (ip text, mac text, vid int, dpid text, port int)')
db.commit()
db.execute('create table flows (dpid text, src_mac text, dest_mac text, action_port int)')
db.commit()
db.execute('create table conv (peer_ip text, out_port int)')
db.commit()
cur = db.cursor()
#Create authorization Token
auth = flare.XAuthToken(user=user,password=passw,controller=server)
my_flare=flare.Api(controller=server,auth=auth)

#Get information from controller
nodesx = my_flare.get_nodes()

#----------------------------------------------------------------------------------------------------
#          Populate SQL nodes table
#----------------------------------------------------------------------------------------------------

for n in nodesx:
	ip = n.ip
	mac = n.mac
	vid = n.vid
	dpid = n.dpid
	port = n.port
	db.execute("INSERT INTO nodes VALUES (?, ?, ?, ?, ?);", (ip, mac, vid, dpid, port))
	db.commit()

#----------------------------------------------------------------------------------------------------
#          Get complete TOE information
#----------------------------------------------------------------------------------------------------
cur.execute("SELECT * FROM nodes WHERE ip ='%s'" % toe_ip)

n = cur.fetchone()

db.commit()

#src_dpid = "00:00:00:00:00:00:00:0d"


src_ip = n[0]
src_mac = n[1]
src_vid = n[2]
src_dpid = n[3]
src_port = n[4]



#----------------------------------------------------------------------------------------------------
#          Populate SQL flow table
#---------------------------------------------------------------------------------------------------

flows = my_flare.get_flows(src_dpid)
	
for f in flows:
	eth_src = f.match.eth_src
	eth_dst = f.match.eth_dst
	action = f.actions.output
	db.execute("INSERT INTO flows VALUES (?, ?, ?, ?);", (src_dpid, eth_src, eth_dst, action))
	db.commit()


#----------------------------------------------------------------------------------------------------
#          Create Dynamic Web Page
#----------------------------------------------------------------------------------------------------

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> FloTapr</title>"
print "</head>"
print "<body background=\"/flowback_red.jpg\" bgcolor=\"#3399ff\" text=\"#ffffff\">"
print "<FORM method='post' ACTION=\"./dd2.py\">"
print "<center><img border=\"0\" src=\"/flowtapper_red.png\" width=\"361\" height=\"74\"></center>"
print "<center><H3> Get In The Middle Of The Conversation</H3></center>" 
print "<HR> "
print "<p>FloTapr is ready to set the flows. Please pick a conversation you would like to listen to.</p>"
print "List of destinations:"
print "<br>"
print "<select name=\"dest_ip\">"
flows = my_flare.get_flows(src_dpid)
for f in flows:
	if (f.match.eth_src == src_mac):
		dest_info = db.execute("SELECT * FROM nodes WHERE mac ='%s'" % f.match.eth_dst)		
		for i in dest_info:
			dest_ip = i[0]
			dest_mac = i[1]
			dest_vid = i[2]
			dest_dpid = i[3]
			dest_port = i[4]
			if (int(dest_port) != int(a_port)):
				print "<option value = \"%s\"> %s </option>" % (dest_ip, dest_ip)
print "</select>"
print " <center><input type=\"submit\" style=\"font-face: 'Comic Sans MS'; font-size: larger; color: black; background-color: #FF0000; border: 3pt ridge lightgrey\" value=\" Set Up Flows\"></center>"
print "<HR>"
print "<textarea name=\"instruct\" cols=\"60\" rows=\"6\">The dropdown list has the IP addresses of all the current conversations with the Target Host. Select the destination IP address and FloTapr will setup the flows to allow capture of the conversation</textarea>"
print "<HR>"
print "<BR>"
print "<BR>"
print "<BR>"
print "<BR>"
print "<BR>"
print "<BR>"
print "<input type=\"hidden\" name=\"toe_ip\" value=%s>" % (toe_ip)
print "<input type=\"hidden\" name=\"src_dpid\" value=%s>" % (src_dpid)
print "<input type=\"hidden\" name=\"src_port\" value=%s>" % (src_port)
print "<input type=\"hidden\" name=\"src_mac\" value=%s>" % (src_mac)
print "<input type=\"hidden\" name=\"a_port\" value=%s>" % (a_port)
print "<input type=\"hidden\" name=\"server\" value=%s>" % (server)
print "<input type=\"hidden\" name=\"user\" value=%s>" % (user)
print "<input type=\"hidden\" name=\"passw\" value=%s>" % (passw)
print "<p>For more information on how to use this application <a href=\"/faq.html\">FloTapr User Guide</a></p>"  
print "<a href=\"/index.html\"><img border=\"0\" src=\"/flowhome_red.png\" width=\"100\" height=\"50\"></a>"
print "<BR>"
print "<BR>"
print "<center><font face=\"Arial\" size=\"1\">SDN Solutions From WookieWare 2014</font></center>"
print "</body>"
print "</html>"


