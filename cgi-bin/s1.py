#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                    dpids
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#
##--------------------------------------------------------------------------
#  Initial release - Pulls VARS from webform. 
#  List datapath identifiers
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

server = "10.132.0.102"
user = "sdn"
passw = "skyline"
#dpid ="00:00:00:00:00:00:00:01"
dpid ="07:d1:00:26:f1:3f:c0:00"
#--------------------------------------------------------------------------
#          IMC factory: Now take the remaining entries in the noimc table
#          and use the eAPI to find addition information about the dpid
#          populate glarn with the added info.
#
#          The remaining entries will be sent to the entry form loader
#          where the additional infor will be manually entered.
#------------------------------------------------------------------------- 

# Auth for imc_passw

auth = hp.XAuthToken(user=user,password=passw,server=server)
api=hp.Api(controller=server,auth=auth)

#Get dpid information from controller
flows= api.get_flows(dpid)
#--------------------------------------------------------------------------
# dpid factory: Break up dpis and match to vendor to determin MAC address
#---------------------------------------------------------------------------
# pad string
#Proc variable is used to tell if noimc db entries have been processed
proc = 0
for f in flows:
 # if f.
  print f

