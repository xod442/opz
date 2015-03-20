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

def varsetup():
  imc_user = 'admin'
  imc_passw = 'admin'
  api_url = 'http://10.132.0.106:8080/imcrs/plat/res/device?size=10000'
  auth=HTTPDigestAuth(imc_user,imc_passw)
  counter = 0
  return (api_url, auth, counter)

def main():
  api_url, auth, counter = varsetup()
  r = requests.get(api_url, auth=auth)

  # Convert xml to dictionary
  my_dict = xmltodict.parse(r.text)

  my_list = my_dict['list']['device']	# makes a list of each device returned from API
  for l in my_list:
	print my_list[counter]['location']
	counter = counter + 1

if __name__ == '__main__':
    sys.exit(main())