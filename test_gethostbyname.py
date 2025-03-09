import socket
import sys



# Print the Python version
print("\n\nPython version:", sys.version)

hostname = socket.gethostname()
server_ip = socket.gethostbyname(hostname)

print('Using gethostbyname(gethostname())')
print(server_ip)

try:
    print('Using gethostbyname(gethostname() + \'.local\')')
    server_ip = socket.gethostbyname(hostname + '.local')
    print(server_ip)
except Exception:
    print("Problem with .local on th is machine")
print("Which ever IP you wish to land on you need to use the associated command above")

