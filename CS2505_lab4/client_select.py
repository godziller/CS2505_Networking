import socket
import sys
import os
import time
import ipaddress
import select

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
        print("Resolved IP address for {}: {}".format(server_domain, server_ip))
        return server_ip
    except socket.gaierror:
        print("Unable to resolve the domain name: {}".format(server_domain))
        sys.exit(1)

def start_client(server_ip, server_port, filename):
    """
    Start the UDP client to send messages to the server and wait for an acknowledgment.
    Implements the stop-and-wait protocol with retransmissions on timeout using select.
    """
    # Create a UDP socket (Datagram socket)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set the socket to non-blocking mode
    client_socket.setblocking(0)

    # Open the file to read
    if not os.path.exists(filename):
        print("File {} not found.".format(filename))
        sys.exit(1)

    with open(filename, 'r') as file:
        for line in file:
            # Remove the newline and any extra spaces
            message = line.strip()

            # Stop-and-wait: send the message and wait for acknowledgment
            while True:
                # Send the message to the server
                print("Sending message: {}".format(message))
                client_socket.sendto(message.encode("utf-8"), (server_ip, server_port))

                # Set the timeout period for select
                timeout = 1  # Timeout period in seconds

                # Use select to monitor the socket for readiness to read
                ready_to_read, _, _ = select.select([client_socket], [], [], timeout)

                if ready_to_read:
                    # If the socket is ready to read, receive the response from the server
                    response, _ = client_socket.recvfrom(2048)
                    print("Server response: {}".format(response.decode()))

                    if response.decode("utf-8") == "ACK":
                        print("Acknowledgment received.")
                        break  # Move to the next message in the file
                else:
                    # If the socket is not ready within the timeout, retransmit the message
                    print("Timeout occurred, retransmitting the message...")

    # Close the socket after communication is done
    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client_2.py <server_domain_or_ip> <filename>")
        sys.exit(1)

    server_address = sys.argv[1]
    filename = sys.argv[2]

    # Check if the provided server address is an IP address or domain name
    if is_valid_ip(server_address):
        server_ip = server_address  # If it's an IP address, use it directly
        print("Using provided IP address: {}".format(server_ip))
    else:
        # Perform DNS lookup for the server domain name
        server_ip = dns_lookup(server_address)

    # Define the server port
    server_port = 6789

    # Start the client communication
    start_client(server_ip, server_port, filename)

