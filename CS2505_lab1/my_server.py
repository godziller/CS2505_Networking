from socket import *
# Create a TCP server socket
# Create a TCP socket using the "socket" method
# Hints: AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP 

server_socket = socket(AF_INET, SOCK_STREAM)

# set values for host 'localhost' - meaning this machine and port number 10000
server_address = ('localhost', 10000)
# output to terminal some info on the address details
print('*** Server is starting up on %s port %s ***' % server_address)
# Bind the socket to the host and port
server_socket.bind(server_address)

while True:
    ...
