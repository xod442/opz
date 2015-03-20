#!/usr/bin/env python
import cgi
import cgitb; cgitb.enable()

def getform():
  """Gets the first and last names from a calling web form."""
  form=cgi.FieldStorage()
  name = form.getvalue('first')
  lname = form.getvalue('last')
  test = "help"
  return (name, lname)
#-------------------------------------------------
def printform(name, lname):
  """Builds a dynameic web page and returns to the users browser"""
  print "Content-type:text/html\r\n\r\n"
  print "<html>"
  print "<head>"
  print "<title> bare bones </title>"
  print "</head>"
  print "<body>"
  print "<hr>"
  print "This is the First name: %s" % (name)
  print "<br>"
  print "This is the Last name: %s" % (lname)
  print "This is the magic %s" % (getform.test())
  print "</body>"
  print "</html>"
  
def main():
  name, lname = getform()
  printform(name, lname)
  
if __name__ == '__main__':
  main()  
