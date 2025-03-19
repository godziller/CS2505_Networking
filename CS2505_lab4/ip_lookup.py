import socket

def get_ip_address(url):
    try:
        ip_address = socket.gethostbyname(url)
        print("The IP address for {} is: {}".format(url, ip_address))
    except socket.gaierror:
        print("Unable to get IP address for {}".format(url))

if __name__ == "__main__":
    url = input("Enter a URL to resolve: ")
    get_ip_address(url)
