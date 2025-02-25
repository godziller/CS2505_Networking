# from the socket module import all
<INSERT CODE TO IMPORT SOCKET MODULE>

# Create a TCP server socket
# Create a TCP socket using the "socket" method
# Hints: AF_INET is used for IPv4 protocols, SOCK_STREAM is used for TCP 
<INSERT CALL TO CREATE THE SOCKET>

# set values for host 'localhost' - meaning this machine and port number 10000
server_address = ('localhost', 10000)
# output to terminal some info on the address details
print('*** Server is starting up on %s port %s ***' % server_address)
# Bind the socket to the host and port
<INSERT CODE TO BIND SERVER ADDRESS TO SOCKET>

# Listen for one incoming connections to the server
<INSERT CODE TO TELL SERVER TO LISTEN FOR ONE INCOMING CONNECTION>

# we want the server to run all the time, so set up a forever true while loop
while True:

    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    # accept() returns an open connection between the server and client, along with the address of the client
    connection, client_address = <INSERT CODE TO ACCEPT THE CONNECTION REQUEST FROM THE CLIENT>
    
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            # decode() function returns string object
            data = connection.recv(16).decode()
            if data:
                print('received "%s"' % data)
                print('sending data back to the client')
                # encode() function returns bytes object
                connection.sendall(data.encode())
            else:
                print('no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        <INSERT CODE TO CLOSE THE CONNECTION>

# now close the socket
<INSERT CODE TO CLOSE THE SOCKET>



# UCC CS2505
