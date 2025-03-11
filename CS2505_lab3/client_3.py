import sys
from socket import *
import ipaddress


# In this functions, I need to reuse Lab2 client to.
# 1.create a client socket
# 2. TCP connect to the server - I now have this info here already from user
# 3. create a message in the HTML format [GET filename http1.1/...)
# 4. then send the message



def do_get(client_socket, ipaddr, port, filename):

    # Construct the HTML request
    # Construct a minimal HTTP/1.1 GET request
    http_get_message = f"GET /{filename} HTTP/1.1\r\n"
    http_get_message += "\r\n"  # End of headers. I need this extra according to the protocol

    # now send the request
    client_socket.sendall(http_get_message.encode())
    return

def do_receive(client_socket):
    response_data = ""  # String buffer to store the full response
    while True:
        chunk = client_socket.recv(1024).decode()  # Decode each chunk immediately
        if not chunk:  # If no more data, exit loop
            break
        response_data += chunk  # Append to buffer
    print(response_data)

def client_setup(server_ip, server_port):
    # Create a TCP client socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Define the server address
    server_address = (server_ip, server_port)


    # Connect to the server
    print(f"Connecting to server at {server_ip} on port {server_port}...")
    client_socket.connect(server_address)
    print("Connection established. Welcome to our web session")
    return client_socket

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <ipaddr> <port> <filename.html>")
        sys.exit(1)

    ipaddr = sys.argv[1]

    # Validate IP address format using ipaddress module
    try:
        ipaddress.IPv4Address(ipaddr)
    except ipaddress.AddressValueError:
        print("Error: Invalid IPv4 address format.")
        sys.exit(1)

    try:
        port = int(sys.argv[2])
        if not (1 <= port <= 65535):
            raise ValueError("Port must be between 1 and 65535.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    filename = sys.argv[3]

    # Validate the file
    if not filename.lower().endswith(".html"):
        print("Error: The file must have a .html extension.")
        sys.exit(1)


    # I don't need a loop this week because its a 1-shot request-response
    # not like the ping-pong of last weeks chat program
    client_socket = client_setup(ipaddr, port)
    do_get(client_socket, ipaddr, port, filename)
    do_receive(client_socket)
