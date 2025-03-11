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
    # This one has all the http protocol trimmings

    http_get_message = (
        "GET /{} HTTP/1.1\r\n"
        "Host: {}:{}\r\n"
        "User-Agent: DarrensWebClient/1.0\r\n"
        "Accept: */*\r\n"
        "Connection: close\r\n"
        "\r\n"  # End of headers
    ).format(filename, ipaddr, port)

    # now send the request
    client_socket.sendall(http_get_message.encode())
    return

def do_receive(client_socket):
    # Receive the response
    response_data = b""
    while True:
        chunk = client_socket.recv(4096)  # Read in chunks
        if not chunk:
            break
        response_data += chunk  # Append to buffer

    # Decode response
    response_text = response_data.decode()

    # Split the response into headers and body
    headers, _, body = response_text.partition("\r\n\r\n")

    # Extract the status line (first line of headers)
    status_line = headers.split("\r\n")[0]

    print("\n🔹 HTTP Response Status:", status_line)
    print("\n🔹 Headers:")
    print(headers)

    print("\n🔹 Body:")
    print(body)  # Print first 500 chars of body (useful for large responses)


def client_setup(server_ip, server_port):
    # Create a TCP client socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Define the server address
    server_address = (server_ip, server_port)


    # Connect to the server
    print("Connecting to server at {} on port {}...".format(server_ip, server_port))
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
        print("Error: {}".format(e))
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
