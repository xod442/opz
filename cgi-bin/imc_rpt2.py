#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    sample_xmltodict.py
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Gets the first 10K devices from an IMC server and makes a report
#  
#
#------Might not need this but please they are handy------------------------ 
#
# Do the imports!!!! 
#----------------------If you dont have it use "apt-get install (name)"
import sys
import xmltodict
import requests
from requests.auth import HTTPDigestAuth
import cgi
import cgitb; cgitb.enable()

def varsetup():
  """ Get the values from the calling web form """
  form = cgi.FieldStorage()
  imc_server = form.getvalue('imc_server')
  imc_user = form.getvalue('imc_user')
  imc_passwd = form.getvalue('imc_passwd')
  # Get 10K devices. Adjust size as necessary
  api_url = 'http://'+imc_server+'/imcrs/plat/res/device?size=10000'
  auth=HTTPDigestAuth(imc_user,imc_passwd)
  counter = 0
  return (api_url, auth, counter)

def pageheader():
  """ Start printing the top of the HTML return page"""
  print ("Content-type:text/html\r\n\r\n")
  print ("<!DOCTYPE html>")
  print ("<html>")
  print ("<head>")
  print ("<title> Wookieware.com</title>")
  print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>")
  print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
  print ("</head>")
  print ("<body>")
  print ("<h1>  IMC API Custom Reporting </h1>") 
  print ("<HR> ")
  print ("<h3> Device Inventory report </h3>")
  print ("<p> This is a listing of the devices currently under inventory in IMC</p>")
  print ("<hr>")
  print ("<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">")
  print ("<tr>")
  print ("<td>devid</td>") 
  print ("<td>label</td>")  
  print ("<td>devip</td>")
  print ("<td>mask</td>")
  print ("<td>status</td>")
  print ("<td>sysName</td>") 
  print ("<td>contact</td>")  
  print ("<td>location</td>")  
  print ("<td>type</td>") 
  print ("<td>model</td>")   
  print ("</tr>")
  
def pagefooter():
  """ Start printing the bottom of the HTML return page"""
  print ("</table>")
  print ("<BR>")
  print ("<BR>")
  print ("<a href=\"/getxapi2.html\">Home</a>")
  print ("<center><font face=\"Arial\" size=\"1\"OneView Solutions From WookieWare 2014</font></center>")
  print ("</body>")
  print ("</html>")

def main():
  pageheader()
  api_url, auth, counter = varsetup()
  r = requests.get(api_url, auth=auth)
  # At this point everything returned s in the variable r.content
  # Convert xml to dictionary
  my_dict = xmltodict.parse(r.text)

  my_list = my_dict['list']['device']	# makes a list of each device returned from API
  for l in my_list:
	devid = my_list[counter]['id']
	label = my_list[counter]['label']
	devip = my_list[counter]['ip']
	mask = my_list[counter]['mask']
	status = my_list[counter]['statusDesc']
	sysName = my_list[counter]['sysName']
	contact = my_list[counter]['contact']
	location = my_list[counter]['location']
	devtype = my_list[counter]['devCategoryImgSrc']
	model = my_list[counter]['typeName']
	print ("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % (devid, 
															              label, 
															              devip, 
															              mask, 
															              status, 
															              sysName, 
															              contact, 
															              location, 
															              devtype, 
															              model))
	counter = counter + 1
  pagefooter()

if __name__ == '__main__':
    sys.exit(main())