from socket import *
import ipaddress

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

# Get the client machine's address (using .local to resolve to local network address)
client_address = gethostbyname(gethostname() + '.local')

# Connect to the server
print(f"Connecting to server at {host_ip} on port {port_number}...")
client_socket.connect(server_address)
print("Connection established.")

# Communication loop
while True:
    try:
        # Get the message from the user
        message = input("Please enter message to send: ")
        message = client_address + ': ' + message  # Prepend the client address
        message += '\n'  # Add newline to indicate message end
        print ("Client> " + message)

        # Send the message to the server
        client_socket.sendall(message.encode())

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
                print(f"Server> " + received_message)
                break

        print("Server response:", received_message.strip())  # Display the server's message

    except KeyboardInterrupt:
        print('Closing socket.')
        break  # Exit the loop and close the connection when interrupted

# Close the socket after communication ends
client_socket.close()
print("Socket closed.")