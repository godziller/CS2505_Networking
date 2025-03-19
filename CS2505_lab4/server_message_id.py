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
    print("Server listening on port {}...".format(server_port))

    while True:
        # Wait to receive a message from the client
        message, client_address = server_socket.recvfrom(2048)

        # Decode the message from bytes to string
        decoded_message = message.decode("utf-8")
        print("Received message: {decoded_message} from {client_address}".format(decoded_message, client_address))

        # Simulate packet loss
        rand = random.randint(1, 10)
        if rand > 5:
            # Extract message ID and original message
            message_id, original_message = decoded_message.split(":", 1)
            print("Processed message ID {}: {}".format(message_id, original_message))

            # Send acknowledgment back with the message ID
            ack_message = "ACK:{}".format(message_id)
            server_socket.sendto(ack_message.encode("utf-8"), client_address)
            print("Sent ACK for message ID {}".format(message_id))
        else:
            print("Simulating packet loss. No response sent.")

if __name__ == "__main__":
    start_server()

