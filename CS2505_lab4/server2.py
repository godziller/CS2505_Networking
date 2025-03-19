import socket
import random

def start_server():
    # Define server host and port
    server_host = "0.0.0.0"  # Listen on all available interfaces
    server_port = 6789

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the address and port
    server_socket.bind((server_host, server_port))
    print(f"Server listening on port {server_port}...")

    while True:
        # Wait to receive a message from the client
        message, client_address = server_socket.recvfrom(2048)

        # Decode the message from bytes to string
        decoded_message = message.decode("utf-8")
        print(f"Received message: {decoded_message} from {client_address}")

        # Simulate 50% packet loss
        rand = random.randint(1, 10)
        if rand > 5:
            # Send the response (ACK) back to the client
            server_socket.sendto("ACK".encode("utf-8"), client_address)
        else:
            print("Simulating packet loss. No response sent.")

if __name__ == "__main__":
    start_server()

