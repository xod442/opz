#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2013 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#=============================================================
# Wookieware Web Update
# Added pages and form handler to permit use with LAMP server
# Version 1.0.0
# Last Update 03/03/2015................Chewie@wookieware.com
#=============================================================


"""
Python program for listing the vms on an ESX / vCenter host
"""

from __future__ import print_function

import pyVmomi

from pyVmomi import vim
from pyVmomi import vmodl

from pyVim.connect import SmartConnect, Disconnect
# from pyVmomi import vmodl

import atexit
import getpass
import cgi
import cgitb; cgitb.enable()
import sys

def getform():
  """ Get the values from the calling web form """
  form = cgi.FieldStorage()
  host = form.getvalue('host')
  user = form.getvalue('user')
  passwd = form.getvalue('passwd')
  port = form.getvalue('port')
  return (host, user, passwd, port)

def printhead(pagevar1, pagevar2, pagevar3, host):
  """
  pagevar1 = Header/Title
  pagevar2 = Subtitle
  pagevar3 = Description text
  host = target vcenter
  """
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
  print ("<p> {} {} </p>".format(pagevar3, host))
  print ("<hr>")
  print ('<table id="tblTasks class=.even">')
  print ("<colgroup>")
  print ('<col width="10%">')
  print ('<col width="25%">')
  print ('<col width="20%">')
  print ('<col width="15%">')
  print ('<col width="15%">')
  print ('<col width="25%">')
  print ("</colgroup>")
  print ("<thead>")
  print ("<tr>")
  print ("<thead>")
  print ("<th>Name</th>")
  print ("<th>Path</th>")
  print ("<th>Guest</th>")
  print ("<th>Annotation</th>")
  print ("<th>State</th>")
  print ("<th>IP Address</th>")
  print ("</tr>")
  print ("</thead>")  

def printfoot(): 
  print ("</table>")
  print ("<nav>") 
  print ('<a href=\"/getallvms.html\" id="button">Home</a>')
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
  print ("$('#tblTasks tbody').on('click', '.deleteRow', function(evt) {") 
  print ("evt.preventDefault();")
  print ("$(evt.target).parents('tr').remove();") 
  print ("});")
  print ("});")
  print ("</script>")
  print ("</main>")
  print ("</section>")
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
  print ('<a href=\"/getallvms.html\" id="button">Home</a>')
  print ("</nav>") 
  print ("<footer>")
  print ("API Connected Solutions From WookieWare 2015")
  print ("</footer")
  print ("</body>")
  print ("</script>")
  print ("</main>")
  print ("</section>")
  print ("</html>")

def PrintVmInfo(vm, depth=1):
   """
   Print information for a particular virtual machine or recurse into a folder
    with depth protection
   """
   maxdepth = 10

   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         PrintVmInfo(c, depth+1)
      return

   summary = vm.summary
   # print table row
   print ("<tr>")
   print ("<td> {} </td>".format(summary.config.name))
   print ("<td> {} </td>".format(summary.config.vmPathName))
   print ("<td> {} </td>".format(summary.config.guestFullName))
   print ("<td> {} </td>".format(summary.config.annotation))
   print ("<td> {} </td>".format(summary.runtime.powerState))
   print ("<td> {} </td>".format(summary.guest.ipAddress))    
   #print ("<td> {} </td>".format(summary.config.ManagedByInfo.type)) 
   print ("</tr>")

def main():
   """
   Simple web driven program for listing the virtual machines on a system.
   """
   
   host, user, passwd, port = getform()
   
   try:
      si = SmartConnect(host=host,
                       user=user,
                       pwd=passwd,
                       port=int(port))

      atexit.register(Disconnect, si)

      content = si.RetrieveContent()
      
      # print the HTML head section
      pagevar1 = "Virtual Machines"
      pagevar2 = "API getAllVms"
      pagevar3 = "This is a list of VM's found on the target"
      printhead(pagevar1, pagevar2, pagevar3, host)
   
      # process machine entries
      for child in content.rootFolder.childEntity:
         if hasattr(child, 'vmFolder'):
            datacenter = child
            vmFolder = datacenter.vmFolder
            vmList = vmFolder.childEntity
            for vm in vmList:
               PrintVmInfo(vm)
      #return 0
      # Print the HTML footer
      printfoot()
   
   except:
      pagevar1 = "Connection Alert"
      pagevar2 = "System Connection failure"
      pagevar3 = "There has been an error connecting to the VMware target"
      pagevar4 = "Check supplied credentials and try again"
      printpage(pagevar1, pagevar2, pagevar3, pagevar4)
      sys.exit()

# Start program
if __name__ == "__main__":
   main()
