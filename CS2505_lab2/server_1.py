# from the socket module import all
from socket import *
from datetime import *

# Create a TCP server socket
# Create a TCP socket using the "socket" method
# Hints: AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP 

server_socket = socket(AF_INET, SOCK_STREAM)
#.local here insures i get the network card ip address, 
#not the local host (127.0.1.1) ip address.
#if i remove + '.local' it will return the 
#127.
#the client has to mirror this even on the same machine.
server_ip = gethostbyname(gethostname()+'.local') 

# set values for host 'localhost' - meaning this machine and port number 10000
# server_address = (server_ip, 10000)
# there are 65k plus potential port numbers. However up to 1024 are typically
# reserved for well agreed services like HTTP(80)
# set port_number to user input -> error check for valid number i.e. int
# enter port number between number (0-65535)

while True:
    try:
        port_number = int(input("Enter Port Number((0-65535)): "))
        break
    except:
        print("Please enter a valid port number(integer)")



server_address = (server_ip, port_number)

# output to terminal some info on the address details
print('*** Server is starting up on %s port %s ***' % server_address)

# print the IP of the local machine
print(f"Currently Serving on Local Machine: {server_ip}")

# Bind the socket to the host and port
# This will tell the operating system to reserve the port number exclusivly
# for my server here. Anyone else trying to use this port number will fail.

server_socket.bind(server_address)

# Listen for one incoming connections to the server

#<INSERT CODE TO TELL SERVER TO LISTEN FOR ONE INCOMING CONNECTION>
server_socket.listen()

#instantiating log.:
log = open('log.md',"w")

# we want the server to run all the time, so set up a forever true while loop
try:
    while True:

        # Now the server waits for a connection
        print('*** Waiting for a connection ***')
        # accept() returns an open connection between the server and client, along with the address of the client. The server will block waiting here. On the client side call to connect() will unblock this 
        now = datetime.now()
        connection, client_address = server_socket.accept()
        
        try:
            print('connection from', client_address)
            #enter logic for log insertion.

            # Receive the data in small chunks and retransmit it
            while True:
                # decode() function returns string object
                data = connection.recv(32).decode()
                if data:
                    print('received from:"%s"' % data)
                    
                    #logic for the server to send messages to client.
                    message = input("Please enter message to send: ")
                    message = str(gethostbyname(gethostname())) + ': ' + message
                    print(message)

                    t = now.strftime("%m/%d/%Y, %H:%M:%S")
                    log.write(f"DATE: {t}, USER: {client_address}, PORT: {port_number}")


                    # encode() function returns bytes object
                    connection.sendall(message.encode())

                else:
                    print('no more data from', client_address)
                    break
                
        finally:
            # Clean up the connection

            #<INSERT CODE TO CLOSE THE CONNECTION>
            connection.close()

except KeyboardInterrupt:
    # now close the socket
    #<INSERT CODE TO CLOSE THE SOCKET>
    print("Server interupted by Ctrl-C, closing socket")
    server_socket.close()
    log.close()


# UCC CS2505

