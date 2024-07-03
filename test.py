# import socket
# import time
# import threading

# PORT = 12345  # Port for broadcasting

# def broadcast_ip():
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#         while True:
#             ip_address = socket.gethostbyname(socket.gethostname())
#             sock.sendto(ip_address.encode(), ('<broadcast>', PORT))
#             time.sleep(5)  # Broadcast every 5 seconds

# def main():
#     broadcast_thread = threading.Thread(target=broadcast_ip)
#     broadcast_thread.start()

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         server_socket.bind(('', PORT))
#         server_socket.listen()

#         print("Waiting for a connection...")
#         client_socket, client_address = server_socket.accept()

#         with client_socket:
#             print("Connected to", client_address)
#             while True:
#                 data = client_socket.recv(1024).decode()
#                 if not data:
#                     break
#                 print("Received:", data)

# if __name__ == "__main__":
#     main()

#  Script to run cmd command and get output in a variable
# import socket
# IPAddr = socket.gethostbyname(socket.gethostname())
 
# print("Your Computer IP Address is:" + IPAddr)
# import subprocess
# output = subprocess.check_output(["arp", "-a","-v"]).decode("utf-8")
# result = output.split("Interface: "+IPAddr)[1].split("\r\n\r\n")[0]
# result_list = result.split("\r\n")
# ip_list = []
# for ip_details in result_list:
#     if ip_details.startswith("  192.168"):
#         ip_item = ip_details.split("      ")[0].replace("  ","")
#         ip_list.append(ip_item)

# print(ip_list)


# from zeroconf import Zeroconf, ServiceInfo
# import socket

# # Get the hostname and IP address of the server
# hostname = socket.gethostname()
# ip_address = socket.gethostbyname(hostname)

# # Create a Zeroconf instance
# zeroconf = Zeroconf()

# # Create a ServiceInfo instance
# info = ServiceInfo(
#     "_myapp._tcp.local.",
#     "MyServerName._myapp._tcp.local.",
#     addresses=[socket.inet_aton(ip_address)],
#     port=12345,
#     properties={"foo": "bar"},  # Add your properties here
# )

# # Register the service
# zeroconf.register_service(info)

# try:
#     print(f"Server started and registered as 'MyServerName' at IP address {ip_address} on port 12345.")
#     input("Press enter to exit...\n")
# finally:
#     zeroconf.unregister_service(info)
#     zeroconf.close()

from scapy.all import ARP, Ether, srp

def scan(ip):
    # Create an ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    # Send the packet and receive the response
    result = srp(arp_request, timeout=3, verbose=0)[0]

    # Extract the IP and MAC addresses from the response
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    
    return devices

# Example usage
target_ip = "192.168.1.1/24"  # Replace with your network range
devices = scan(target_ip)

for device in devices:
    print(f"IP Address: {device['ip']}, MAC Address: {device['mac']}")
