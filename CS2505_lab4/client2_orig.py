from socket import *
import time 
import sys

def start_client(server_domain, file_name):
    
    server_ip = gethostbyname(server_domain)
    server_address = (server_ip, 6789)

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(1)

    try:
        with open(file_name, 'r') as file:
            for line in file:
                message = line.strip()
                while True:
                    try:
                        print("Sent to server: {}".format(message))
                        client_socket.sendto(message.encode(), server_address)

                        response, _ = client_socket.recvfrom(4096)
                        print("Recieved from server: {}".format(response.decode()))

                        break

                    except TimeoutError:
                        print("Timeout: Retrying message: {}".format(message))

                        continue
    except FileNotFoundError:
        print("Error: File {} not found.".format(file_name))
    finally:
        client_socket.close()




if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client_2.py <server_domain> <file_name>")
    else:
        start_client(sys.argv[1], sys.argv[2])
