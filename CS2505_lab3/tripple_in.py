import sys
import os
import ipaddress


# In this functions, I need to reuse Lab2 client to.
# 1.create a client socket
# 2. TCP connect to the server - I now have this info here already from user
# 3. create a message in the HTML format [GET filename http1.1/...)
# 4. then send the message



def do_get(ipaddr, port, filename):
    print(ipaddr)
    print(port)
    print(filename)

def do_receive():
    pass

def client_setup():
    pass
# Thinking of reusing last week
# but can rip out a lot of the user input part
# add the ip and port to the function above
# then return my client socket so I can use it in the send/receive parts

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
    do_get(ipaddr, port, filename)
    do_receive()
