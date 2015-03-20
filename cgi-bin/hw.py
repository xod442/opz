#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    "hello wolrd test"
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
#-------------------------------------------------------------------------
#   Uncomment the next line to turn on python debugging
#  	import pdb; pdb.set_trace()
#-------------------------------------------------------------------------
#
#-------------------------------------------------------------------------
#              Get the field VARS from the calling HTML form
#-------------------------------------------------------------------------
form = cgi.FieldStorage()
text = form.getvalue('text')
#----------------------------------------------------------------------------------------------------
#          Create Dynamic Web Page
#----------------------------------------------------------------------------------------------------

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<!-- This is a comment -->"
print "<title> Page Title</title>"
print "</head>"
print "<body>"
print "<FORM method='post' ACTION=\"./hello_world.py\">"
print "<h3> This is what you entered in the form</h3>" 
print "Text: <textarea rows=\"1\" cols=\"50\">%s</textarea>" % (text)
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

