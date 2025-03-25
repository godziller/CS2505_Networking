import random 
from socket import *
import sys

def udp_ping_client(port, loss_rate=0.3):

    # Create UDP socket
    server_socket = socket(AF_INET, SOCK_DGRAM)

    # Bind the socket to the port
    server_socket.bind(('',port))
    print(f"Ping server listening on port {port} with packet loss rate {loss_rate*100}%")

    try:
        while True:

            # Recieve message from client
            message, client_address = server_socket.recvfrom(1024)

            # Simulate packet loss
            if random.random() < loss_rate:
                print(f"Packet from {client_address} dropped.")
                continue

            # Echo the message back to the client
            server_socket.sendto(message,  client_address)
            print(f"Echoed packet to {client_address}")

    except KeyboardInterrupt:
        print("\nServer shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)


    try:
        port = int(sys.argv[1])
        udp_ping_client(port)

    except ValueError:
        print("Port must be a valid integer")
        sys.exit(1)
