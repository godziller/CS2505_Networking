# from the socket module import all
from socket import *
import ipaddress

# Create a TCP socket using the "socket" method
# Hints: AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP 
#<INSERT CALL TO CREATE THE SOCKET>
client_socket = socket(AF_INET, SOCK_STREAM)

# If i want my client to talk to a server on a different machine i will have to
# hard code the server ip address here... host_ip = xxx.xxx.xxx.xxx
# below only works with the client and server on the same machine USING
# the actual ip address (not the loopback address)

#host_ip = gethostbyname(gethostname()+".local")

while True:
    try: 
        host_ip = input("Enter the server address to connect to: ")
        ipaddress.ip_address(host_ip)
        break
    except:
        print('Please enter valid server IP')

# set values for host 'localhost' - meaning this machine and port number 10000
# the machine address and port number have to be the same as the server is using.
# read user input for port number 

while True:
    try:
        port_number = int(input("Enter the Server's Port Number: "))
        break
    except:
        print("Please enter a valid port number(integer)")

server_address = (host_ip, port_number)

# output to terminal some info on the address details
print('connecting to server at %s port %s' % server_address)
# Connect the socket to the host and port
#<INSERT CALL TO CONNECT TO SERVER>
client_socket.connect(server_address)

while True:
    try:
    
        # Send data
        #message = 'This is the message from the client to the server.'
        #read input
        
        message = input("Please enter message to send: ")
        message = gethostbyname(gethostname())+'.local' + ': ' + message
        
        # Data is transmitted to the server with sendall()
        # encode() function returns bytes object
        client_socket.sendall(message.encode())

        # Look for the response
        recieved_message = ""

        #this chunk of code with go around until it reads a string with '\n' (i.e the last byte sent) we then concatonate all things.
        while True:
    	    # Data is read from the connection with recv()
            # decode() function returns string object
            data = client_socket.recv(32).decode()
            if "\n" in data:
                recieved_message += data
                break
            else:
                recieved_message += data
        print(recieved_message)


    except KeyboardInterrupt:
        print('closing socket')
        # <INSERT CALL TO CLOSE SOCKET>
        client_socket.close()



# UCC CS2505

