# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 9047
server_ip = gethostbyname(gethostname() + '.local')
# Bind the socket to server address and server port
serverSocket.bind((server_ip, serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

try: # Adding this try block, so I can catch a ctrl-c and unbind from socket gracefully

    # Server should be up and running and listening to the incoming connections
    while True:
        print('Ready to serve...')

        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()

        # If an exception occurs during the execution of try clause
        # the rest of the clause is skipped
        # If the exception type matches the word after except
        # the except clause is executed
        try:
            # Receives the request message from the client
            message = connectionSocket.recv(1024).decode()

            # First job - check if the client sent a 3-part message.
            # The ultimate format would be [METHOD PATH VERSION]
            # But here I just want to check 3 parts came in...

            # Slide 33 of Appliction Layer deck
            # request_lines is the entire message broken by carriage return/line feed
            request_lines = message.split("\r\n")  # Split request into lines

            # this fisrt line [0] is the 'request line' - [Method File VERSION]
            request_parts = request_lines[0].split()  # First line is the request line

            if len(request_parts) < 3:
                # Client sent a malformed request.
                connectionSocket.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
                connectionSocket.send("<html><body><h1>400 Bad Request</h1></body></html>\r\n".encode())
                connectionSocket.close()
                continue  # Continue serving - client problem, not server problem.

            # Extract parts safely
            method = request_parts[0].upper()  # Convert method to uppercase
            filename = request_parts[1].lstrip("/")  # Remove the leading '/'
            http_version = request_parts[2]

            # Now let's extract extra headers
            headers = {}
            for header_line in request_lines[1:]:  # Skip the first line (request line)
                if header_line.strip() == "":  # Stop at empty line (headers end)
                    break
                key, value = header_line.split(":", 1)  # Split only on first ":"
                headers[key.strip()] = value.strip()

            # Debug: Print extracted headers
            print("🔹 Extracted Headers:", headers)

            # Check if User-Agent exists
            # Slide 32 of app-layer deck
            user_agent = headers.get("User-Agent", "Unknown")
            print("🔹 User-Agent: {}".format(user_agent))
            # Validate HTTP method (must be "GET")
            if method != "GET":
                connectionSocket.send("HTTP/1.1 400 Bad Request\r\n\r\n".encode())
                connectionSocket.send("<html><body><h1>400 Bad Request</h1></body></html>\r\n".encode())
                connectionSocket.close()
                continue  # Go back to waiting for new connections

            # Validate HTTP version (must be "HTTP/1.1")
            if http_version != "HTTP/1.1":
                connectionSocket.send("HTTP/1.1 505 HTTP Version Not Supported\r\n\r\n".encode())
                connectionSocket.send("<html><body><h1>505 HTTP Version Not Supported</h1></body></html>\r\n".encode())
                connectionSocket.close()
                continue  # Go back to waiting for new connections

            # This is the file check
            # NOTE - THIS IS WHAT WILL RAISE THE IOError below!!
            with open(filename, 'r') as f:
                # Store the entire contenet of the requested file in a temporary buffer
                outputdata = f.read()
            # Send the HTTP response header line to the connection socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

            # Send the content of the requested file to the connection socket
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

        except IOError:
            # Send HTTP response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        finally:
            # Close client connection
            # Dropping all my closes down to this finally block..
            connectionSocket.close()

except KeyboardInterrupt:
    print("\nShutting down server gracefully...")
    serverSocket.close()

