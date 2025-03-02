# from the socket module import all
from socket import *

# Create a TCP socket using the "socket" method
# Hints: AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP 
#<INSERT CALL TO CREATE THE SOCKET>
client_socket = socket(AF_INET, SOCK_STREAM)

# If i want my client to talk to a server on a different machine i will have to
# hard code the server ip address here... host_ip = xxx.xxx.xxx.xxx
# below only works with the client and server on the same machine USING
# the actual ip address (not the loopback address)

host_ip = gethostbyname(gethostname())

# set values for host 'localhost' - meaning this machine and port number 10000
# the machine address and port number have to be the same as the server is using.
server_address = (host_ip, 10000)
# output to terminal some info on the address details
print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port
#<INSERT CALL TO CONNECT TO SERVER>
client_socket.connect(server_address)

try:
    
    # Send data
    #message = 'This is the message from the client to the server.'
    message = input("Please enter message to send: ")
    print(f"sending: {message} ")
    print('sending "%s"' % message)
    # Data is transmitted to the server with sendall()
    # encode() function returns bytes object
    client_socket.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
    	# Data is read from the connection with recv()
        # decode() function returns string object
        data = client_socket.recv(16).decode()
        amount_received += len(data)
        print('received "%s"' % data)

finally:
    print('closing socket')
   # <INSERT CALL TO CLOSE SOCKET>
    client_socket.close()



# UCC CS2505

