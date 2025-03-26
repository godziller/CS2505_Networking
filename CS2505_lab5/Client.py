import socket
import sys
import datetime
import math

def calculate_statistics(rtt_list):
    if not rtt_list:
        return 0.0, 0.0, 0.0, 0.0
    
    min_rtt = min(rtt_list)
    max_rtt = max(rtt_list)
    avg_rtt = sum(rtt_list) / len(rtt_list)
    stddev = math.sqrt(sum((x - avg_rtt)**2 for x in rtt_list) / len(rtt_list))

    return min_rtt, max_rtt, avg_rtt, stddev

def udp_ping_client(server_ip, server_port, count=10):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)  # 1 second timeout
    
    rtt_list = []
    packets_lost = 0
    
    print("PING {} using UDP".format(server_ip))
    
    for sequence in range(1, count + 1):
        send_time = datetime.datetime.now()

        # This is where I think I would put my Student ID
        message = f"Ping {sequence} {send_time.timestamp()}".encode()
        
        try:
            client_socket.sendto(message, (server_ip, server_port))
            
            try:
                response, server_address = client_socket.recvfrom(1024)
                receive_time = datetime.datetime.now()
                rtt = (receive_time - send_time).total_seconds() * 1000
                
                decoded = response.decode()
                if decoded.startswith(f"Ping {sequence}"):
                    print("{} bytes from {}: udp_seq={} time={:.3f} ms".format(len(response), server_address[0], sequence,rtt))
                    rtt_list.append(rtt)
                else:
                    print("Received corrupted packet from {}".format(server_address[0]))
                    packets_lost += 1
                    
            except socket.timeout:
                print("Request timed out.")
                packets_lost += 1
                
        except Exception as e:
            print("Error sending packet: {}".format(e))
            packets_lost += 1
    
    # Print statistics
    print("\n--- {} ping statistics ---".format(server_ip))
    packets_sent = count
    packets_received = packets_sent - packets_lost
    loss_percentage = (packets_lost / packets_sent) * 100 if packets_sent > 0 else 0
    
    print("{} packets transmitted, {} received, {:.2f}% packet loss".format(packets_sent, packets_received, loss_percentage))
    
    if rtt_list:
        min_rtt, max_rtt, avg_rtt, stddev = calculate_statistics(rtt_list)
        print("round-trip min/avg/max/stddev = {:.3f}/{:.3f}/{:.3f}/{:.3f} ms".format(min_rtt, avg_rtt, max_rtt, stddev))

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python UDP_ping_Client.py <count> <server_ip>")
        sys.exit(1)
    
    try:
        count = int(sys.argv[1])
        server_ip = sys.argv[2]
        server_port = 12000  # Must match server port
        
        udp_ping_client(server_ip, server_port, count)
    except ValueError:
        print("Error: Count must be an integer")
        sys.exit(1)
