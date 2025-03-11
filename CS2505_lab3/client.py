#import socket
from socket import *
import sys
import ipaddress

def client_setup(server_host, server_port):
    # Create TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Get a valid server IP address from the user
    server_address = (server_host, server_port)

    #Connecting to the server
    print(f"Connecting to server at {server_host} on port {server_port}")
    client_socket.connect(server_address)
    print("Connection Esatblished")
    return client_socket

# def send_message()
def send_message(client_socket, filepath):

    message = f"GET /{filepath} HTTP/1.1\r\n"
    message += "\r\n"

    print(f"Sending Message {message}")
    client_socket.sendall(message.encode())

    
# def recieve_message()
def recieve_message(connection_socket):
    # Create a buffer to store/build our data as it comes in
    data_buffer = ""
    while True:
        chunk = client_socket.recv(1024).decode()
        if not chunk:
            break
        data_buffer += chunk

    # Print recieved data.
    print(data_buffer)



if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Please enter the correct amount of inputs")
        sys.exit(1)

    #get client ip
    client_address = gethostbyname(gethostname())

    # extract data from the argument
    # Getting server address
    server_host = sys.argv[1]
 
    # Getting server port
    server_port = int(sys.argv[2])
        
    # Getting the filepath    
    filepath = sys.argv[3]
        
    # Client Setup
    client_socket = client_setup(server_host, server_port)

    send_message(client_socket, filepath)
    recieve_message(client_socket)

    print("Closing Application")
