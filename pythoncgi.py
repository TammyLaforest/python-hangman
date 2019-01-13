import cgitb
cgitb.enable(display=0, logdir="/path/to/logdir")


#!/usr/local/bin/python
print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print (<title>Hello World - First CGI Program</title>)
print ('</head>')
print ('<body>')
print ('<h2>Hello World! this is my first CGI Program</h2>')
print ('</body>')
print ('</html>')

form = cgi.FieldStorage()
if "name" not in form or "addr" not in form:
    print("<H1>Error</H1>")
    print("Please fill in the name and addr fields.")
    return
print("<p>name:", form["name"].value)
print("<p>addr:", form["addr"].value)