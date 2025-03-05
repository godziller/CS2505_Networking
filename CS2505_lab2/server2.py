from socket import *
from datetime import datetime


def server_setup():
    # Open log file to log server activity

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
    # Now the server waits for a connection
    print('*** Waiting for a connection ***')
    # Accept an incoming connection (this call will block until a connection is made)
    client_connection, client_address = server_socket.accept()
    print(f'Connection established from {client_address}')
    return client_connection, server_socket, server_ip

def receive_message(client_connection):
    received_message = ""

    while True:
        try:
            # Receive data in chunks from the client
            data = client_connection.recv(32).decode()  # Decode to string

            if not data:  # If no data is received, client may have closed the connection
                print(f"No more data from client")
                break

            # Append the received data to the message
            received_message += data

            # If a newline is detected, consider the message fully received
            if '\n' in received_message:
                print(f"Client> " + received_message.strip())
                break

             # Log the timestamp of the received message
            t = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            log.write(f"DATE: {t}, USER: Client, MESSAGE: {received_message}\n")

        except Exception:
            print("Ctrl C... exiting")
            raise

def send_message(client_connection, server_ip):
    try:

    # Ask the server operator for a message to send back to the client
        message = input("Server enter message to send: ")
        message = server_ip + ': ' + message
        message += '\n'

        # Send the message back to the client
        client_connection.sendall(message.encode())
    except KeyboardInterrupt:
        print("Ctrl C... exiting")
        raise Exception

if __name__ == '__main__':

    log = open('log.txt', "w")

    client_connection, server_socket, server_ip = server_setup()

    while True:
        try:
            receive_message(client_connection)
            # only using server_ip here to add to the message, nothing else
            send_message(client_connection, server_ip)


        except Exception:

            print("Server interrupted by Ctrl-C, closing socket.")
            client_connection.close()
            server_socket.close()
            log.close()
            break

    print("Server shut down successfully.")





