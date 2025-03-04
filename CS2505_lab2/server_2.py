from socket import *
from datetime import datetime

# Create a TCP server socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Obtain the local IP address using '.local' to avoid using localhost (127.0.1.1)
server_ip = gethostbyname(gethostname() + '.local')

# Ask the user for a valid port number between 0 and 65535
while True:
    try:
        port_number = int(input("Enter Port Number (0-65535): "))
        if 0 <= port_number <= 65535:
            break
        else:
            print("Port number must be between 0 and 65535. Try again.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

server_address = (server_ip, port_number)

# Output some information to the terminal about the server's setup
print(f'*** Server is starting up on {server_ip} port {port_number} ***')
print(f"Currently Serving on Local Machine: {server_ip}")

# Bind the server socket to the provided address and port
server_socket.bind(server_address)

# Listen for incoming connections (allowing up to 5 pending connections)
server_socket.listen(5)

# Open log file to log server activity
log = open('log.txt', "w")

try:
    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    # Accept an incoming connection (this call will block until a connection is made)
    connection, client_address = server_socket.accept()
    print(f'Connection established from {client_address}')

    while True:
        try:
            # Initialize an empty string to store the received message
            received_message = ""

            while True:
                # Receive data in chunks from the client
                data = connection.recv(32).decode()  # Decode to string

                if not data:  # If no data is received, client may have closed the connection
                    print(f"No more data from {client_address}")
                    break

                # Append the received data to the message
                received_message += data

                # If a newline is detected, consider the message fully received
                if '\n' in received_message:
                    print(f"Server> " + received_message)
                    break

            # Log the timestamp of the received message
            t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            log.write(f"DATE: {t}, USER: {client_address}, PORT: {port_number}, MESSAGE: {received_message}\n")

            # Ask the server operator for a message to send back to the client
            message = input("Please enter message to send: ")
            print(f"ME> {message}")

            # Prepend the server's IP address to the message
            message = f"{gethostbyname(gethostname() + '.local')}: {message}"

            # Send the message back to the client
            connection.sendall(message.encode())

        except Exception as e:
            print(f"Error while handling data: {e}")
            break

except KeyboardInterrupt:
    print("Server interrupted by Ctrl-C, closing socket.")

finally:
    # Clean up the connections and close the server socket and log file
    connection.close()
    server_socket.close()
    log.close()
    print("Server shut down successfully.")

