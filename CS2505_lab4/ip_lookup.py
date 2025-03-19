import socket

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        print(f"The IP address for {url} is: {ip_address}")
    except socket.gaierror:
        print(f"Unable to get IP address for {url}")

if __name__ == "__main__":
    url = input("Enter a URL to resolve: ")
    get_ip_address(url)
