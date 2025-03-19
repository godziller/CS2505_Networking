import socket
import random

def start_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the port
    server_address = ('localhost', 6789)
    server_socket.bind(server_address)
    print("Server listening on {}...".format(server_address))

    while True:
        # Receive message from client
        data, client_address = server_socket.recvfrom(4096)
        data = data.decode()
        print("Received message from {}: {}".format(client_address, data))

        # Simulate 50% packet loss
        rand = random.randint(1, 10)
        if rand > 5:
            # Convert message to uppercase
            modified_message = data.upper()

            # Send the modified message back to the client
            print("Sent response to {}: {}".format(client_address, modified_message))
            server_socket.sendto(modified_message.encode(), client_address)

        else:
            print("Simulated packet loss for message: {}".format(data))

if __name__ == "__main__":
    start_server()
