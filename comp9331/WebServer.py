import socket
import sys
from re import *

#use python 2

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: python TCP webserver  <server port no>")
    sys.exit()
	
#create socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost',int(sys.argv[1])))
sock.listen(1)
print('The Server is ready to receive')

#infinite loop to get client request
while True:
	connection, client_address=sock.accept()
	print 'Got connection from: ', client_address
	try:
		#receive the message, parse the document name
		message=connection.recv(2048)
		file=message.split()[1]
		print file
		print file[1:-1]
		#open and read the document
		f=open(file[1:-1])
		data=f.read()
		
		#send the header
		connection.send("HTTP/1.1 200 OK\r\n\r\n")
		
		#send the file line by line 	
		for i in data:  
			connection.send(i)
		connection.send("\r\n")
		
		# Close the client connection socket
		connection.close()
		

	except IOError:
		connection.send("HTTP/1.1 404 Not Found\r\n\r\n")
		connection.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
		# Close the client connection socket
		connection.close()
sock.close()
	
		