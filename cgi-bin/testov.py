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
  name = form.getvalue('name')
  return (host, user, passwd, cert, proxy, name)
  
def printhead(pagevar1, pagevar2, pagevar3):
   print ("Content-type:text/html\r\n\r\n")
   print ("<!DOCTYPE html>")
   print ("<html>")
   print ("<head>")
   print ("<title> Wookieware.com</title>")
   print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/tasks.css\"/>")
   print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
   print ("</head>")
   print ("<body>")
   print ("<header>")
   print ("<span>  {} </span>".format(pagevar1)) 
   print ("</header>")
   print ("<main>")
   print ('<section id="mainDisplay">')
   print ("<h3> {} </h3>".format(pagevar2))
   print ("<p> {} </p>".format(pagevar3))
   print ("<hr>")
   print ('<table id="tblTasks class=.even">')
   print ("<colgroup>")
   print ('<col width="30%">')
   print ('<col width="30%">')
   print ('<col width="30%">')
   print ("</colgroup>")
   print ("<thead>")
   print ("<tr>")
   print ("<thead>")
   print ("<th>Name</th>")
   print ("<th>Vlan</th>")
   print ("<th>Type</th>")
   print ("</tr>")
   print ("</thead>")  

def printfoot(): 
  print ("</table>")
  print ("<nav>") 
  print ('<a href=\"/getnet1.html\" id="button">Home</a>')
  print ("</nav>") 
  print ("<footer>")
  print ("API Connected Solutions From WookieWare 2015")
  print ("</footer")
  print ("</body>")
  print ("<script>")
  print ("$(document).ready(function() {")
  print ("$('tbody tr:even').addClass('even');")
  print ("$('tbody tr').click(function(evt) {")
  print ("$(evt.target).closest('td').siblings().andSelf().toggleClass('rowHighlight');")
  print ("});")
  print ("});")
  print ("</script>")
  print ("</section>")
  print ("</main>")
  print ("</html>")

def printpage(pagevar1, pagevar2, pagevar3, pagevar4):
  # Genic return page
  print ("Content-type:text/html\r\n\r\n")
  print ("<!DOCTYPE html>")
  print ("<html>")
  print ("<head>")
  print ("<title> Wookieware.com</title>")
  print ("<link rel=\"stylesheet\" type\"text/css\" href=\"../../css/tasks.css\"/>")
  print ("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js\"></script>")
  print ("</head>")
  print ("<body>")
  print ("<header>")
  print ("<span>  {} </span>".format(pagevar1)) 
  print ("</header>")
  print ("<main>")
  print ('<section id="mainDisplay">')
  print ("<h3> {} </h3>".format(pagevar2))
  print ("<p> {} </p>".format(pagevar3))
  print ("<p> {} </p>".format(pagevar4))
  print ("<nav>") 
  print ('<a href=\"/getnet1.html\" id="button">Home</a>')
  print ("</nav>") 
  print ("<footer>")
  print ("API Connected Solutions From WookieWare 2015")
  print ("</footer")
  print ("</body>")
  print ("</script>")
  print ("</main>")
  print ("</section>")
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
        pagevar4 = e
        printpage(pagevar1, pagevar2, pagevar3, pagevar4)
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

def getnet(net, name):
    if name:
        enets = net.get_enet_networks()
        pagevar1 = "Network Listing"
        pagevar2 = "API get-networks"
        pagevar3 = "This is the response from a get networks API GET request"
        printhead(pagevar1, pagevar2, pagevar3)
        # Used for test variable handoff
        #print ("<td> {} {} {} {} {} {} </td>".format(host, user, passwd, cert, proxy, name)) 
        for enet in enets:
          namex = enet['name']
          vlanx = enet['vlanId']
          typex = enet['ethernetNetworkType']
          print ("<tr>")
          #print (" <td> {} </td> ".format(enet))
          # Used for displaying complete API return contents
          print ("<td> {} </td> <td> {} </td> <td> {} </td>".format(namex, vlanx, typex))
          print ("</tr>")
          
            #if enet['name'] == name:
                #pprint(enet)
        printfoot()
  
def main():
     # Arguments supplied from getform function
    host, user, passwd, cert, proxy, name = getform()
    
    credential = {'userName': user, 'password': passwd}

    con = hpov.connection(host)
    net = hpov.networking(con)

    if proxy:
        con.set_proxy(proxy.split(':')[0], proxy.split(':')[1])
    if cert:
        con.set_trusted_ssl_bundle(cert)

    login(con, credential)
    acceptEULA(con)

    getnet(net, name)
   
if __name__ == '__main__':
    sys.exit(main())

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
