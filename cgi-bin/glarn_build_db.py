#!/usr/bin/env python
#--------------------------------------------------------------------------
#
#                   glarn database builder
#                    Rick Kauffman a.k.a. Chewie
#
#                    Hewlett Packard Company    Revision: 1.0
#                   ~~~~~~~~~ WookieWare ~~~~~~~~~~~~~
#      Change history....09/03/2014
#
#

import sqlite3

#  	import pdb; pdb.set_trace()
#

#------------------------------------------------------------------------------
#          Create glarn database and tables
#-----------------------------------------------------------------------------
db = sqlite3.connect('/var/www/html/glarn.db')
db.execute('drop table if exists dpid')
db.execute('drop table if exists noimc')
db.execute('drop table if exists chozr')
db.execute('create table dpid (dpid text primary key, mac text, ip text, sysName text, contact text, location text, id int, vendor text, sel int)')
db.commit()
db.execute('create table noimc (dpid text primary key, devip text, mac text, vendor text, proc int)')
db.commit()
db.execute('create table chozr (dpid text primary key, devip text, mac text, vendor text, proc int)')
db.commit()
cur = db.cursor()

