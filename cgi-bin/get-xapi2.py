#!/usr/bin/env python3
###
# (C) Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
###
import sys
if sys.version_info < (3, 2):
    raise Exception('Must use Python 3.2 or later')
import hpOneView as hpov
from pprint import pprint
import cgi
import cgitb; cgitb.enable()

def getform():
  """ Get the values from the calling web form """
  form = cgi.FieldStorage()
  host = form.getvalue('host')
  user = form.getvalue('user')
  passwd = form.getvalue('passwd')
  cert = form.getvalue('cert')
  proxy = form.getvalue('proxy')
  return (host, user, passwd, cert, proxy)
  
def printpage(pagevar1, pagevar2, pagevar3, pagevar4):
  """
  pagevar1 = Header/Title
  pagevar2 = Subtitle
  pagevar3 = Description text
  pagevar4 = Message Body
  """
  print ("Content-type:text/html\r\n\r\n")
  print ("<!DOCTYPE html>")
  print ("<html>")
  print ("<head>")
  print ("<title> Wookieware.com</title>")
  print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/corex.css\"/>")
  print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
  print ("</head>")
  print ("<body>")
  print ("<h1>  {} </h1>".format(pagevar1)) 
  print ("<HR> ")
  print ("<h3> {} </h3>".format(pagevar2))
  print ("<p> {} </p>".format(pagevar3))
  print ("<hr>")
  print ("<table border=\"1\" cellpadding=\"10\" class=\"TFtable\">")
  print ("<tr>")
  print ("<td> {} </td>".format(pagevar4)) 
  print ("</tr>")
  print ("</table>")
  print ("<BR>")
  print ("<BR>")
  print ("<a href=\"/getxapi2.html\">Home</a>")
  print ("<center><font face=\"Arial\" size=\"1\"OneView Solutions From WookieWare 2014</font></center>")
  print ("</body>")
  print ("</html>")


def acceptEULA(con):
    # See if we need to accept the EULA before we try to log in
    con.get_eula_status()
    try:
        con.set_eula('no')
    except Exception as e:
        pagevar1 = "EULA EXCEPTION ERROR"
        pagevar2 = "EULA exception error occured"
        pagevar3 = "There has been an unknown issue in the processing"
        printpage(pagevar1, pagevar2, pagevar3, e)
        sys.exit()
        #
        # print('EXCEPTION:')
        # print(e)

def login(con, credential):
    # Login with givin credentials
    try:
        con.login(credential)
    except:
        pagevar1 = "Login failed"
        pagevar2 = "Credential check failure"
        pagevar3 = "There has been an error with the credentials you suppllied"
        pagevar4 = "Login Failed - Use back button"
        printpage(pagevar1, pagevar2, pagevar3, pagevar4)
        sys.exit()

def getapi(sts):
    version = sts.get_version()
    pagevar1 = "XAPI Version"
    pagevar2 = "Version information"
    pagevar3 = "The current version of the XAPI on the OneView server"
    printpage(pagevar1, pagevar2, pagevar3, version)
    #
    #print('currentVersion: ', version['currentVersion'])
    #print('minimumVersion: ', version['minimumVersion'])


def main():
    # Arguments supplied from getform function
    host, user, passwd, cert, proxy = getform()

    credential = {'userName': user, 'password': passwd}

    con = hpov.connection(host)
    sts = hpov.settings(con)

    if proxy:
        con.set_proxy(proxy.split(':')[0], proxy.split(':')[1])
    if cert:
        con.set_trusted_ssl_bundle(cert)

    login(con, credential)
    acceptEULA(con)

    getapi(sts)
   
if __name__ == '__main__':
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
