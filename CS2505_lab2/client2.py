from socket import *
import ipaddress




def client_setup():
    # Create a TCP client socket
    client_socket = socket(AF_INET, SOCK_STREAM)

    # Get a valid server IP address from the user
    while True:
        try:
            host_ip = input("Enter the server address to connect to: ")
            ipaddress.ip_address(host_ip)  # Validate the IP format
            break
        except ValueError:
            print("Please enter a valid server IP.")

    # Get the server's port number
    while True:
        try:
            port_number = int(input("Enter the Server's Port Number: "))
            break
        except ValueError:
            print("Please enter a valid port number (integer).")

    # Define the server address
    server_address = (host_ip, port_number)


    # Connect to the server
    print(f"Connecting to server at {host_ip} on port {port_number}...")
    client_socket.connect(server_address)
    print("Connection established. Welcome to our chat")
    return client_socket

def send_message(client_socket, from_client_prompt):
    # Get the message from the user
    message = input("Client> : ")
    message = from_client_prompt + ': ' + message  # Prepend the client address
    message += '\n'  # Add newline to indicate message end
    client_socket.sendall(message.encode())

def receive_message(client_socket):
    # Receive the response from the server
    received_message = ""
    while True:
        data = client_socket.recv(32).decode()  # Decode to string

        if not data:  # If no data is received, client may have closed the connection
            print(f"No more data from {client_address}")
            break

        # Append the received data to the message
        received_message += data

        # If a newline is detected, consider the message fully received
        if '\n' in received_message:
            print(f"Server> " + received_message.strip())
            break

if __name__ == '__main__':
    client_socket = client_setup()

    while True:
        try:
            # Get the client machine's address (using .local to resolve to local network address)
            # I don't need this for anything other than a prompt to server
            client_address = gethostbyname(gethostname() + '.local')

            send_message(client_socket, client_address)

            receive_message(client_socket)



        except Exception:
            print('Closing socket.')
            client_socket.close()
            break

    print("Closing Application")

