import socket
import sys
import os
import ipaddress

def is_valid_ip(ip):
    """
    Check if the given string is a valid IP address (IPv4 or IPv6).
    """
    try:
        # Try to create an IP address object using ipaddress module
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def dns_lookup(server_domain):
    """
    Perform DNS lookup for the given server domain name.
    """
    try:
        server_ip = socket.gethostbyname(server_domain)
        print(f"Resolved IP address for {server_domain}: {server_ip}")
        return server_ip
    except socket.gaierror:
        print(f"Unable to resolve the domain name: {server_domain}")
        sys.exit(1)

def start_client(server_ip, server_port, filename):
    """
    Start the UDP client to send messages to the server and receive responses.
    """
    # Create a UDP socket (Datagram socket)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Open the file to read
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        sys.exit(1)

    with open(filename, 'r') as file:
        for line in file:
            # Remove the newline and any extra spaces
            message = line.strip()

            # Send the message to the server
            client_socket.sendto(message.encode("utf-8"), (server_ip, server_port))

            # Receive the server's response
            response, _ = client_socket.recvfrom(2048)
            print(f"Server response: {response.decode('utf-8')}")

    # Close the socket after communication is done
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client_1.py <server_domain_or_ip> <filename>")
        sys.exit(1)

    server_address = sys.argv[1]
    filename = sys.argv[2]

    # Check if the provided server address is an IP address or domain name
    if is_valid_ip(server_address):
        server_ip = server_address  # If it's an IP address, use it directly
        print(f"Using provided IP address: {server_ip}")
    else:
        # Perform DNS lookup for the server domain name
        server_ip = dns_lookup(server_address)

    # Define the server port
    server_port = 6789

    # Start the client communication
    start_client(server_ip, server_port, filename)

