import socket

ip = '127.0.0.1'
port = 5802
print(ip, " ", port)

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("Do Ctrl+c to exit the program !!")

# Let's send data through UDP protocol
# while True:
send_data = input("Type some text to send =>")
s.sendto(send_data.encode(), (ip, port))
print("\n\n 1. Client Sent : ", send_data, "\n\n")
data, address = s.recvfrom(4096)
print("\n\n 2. Client received : ", data.decode(), "\n\n")
# close the socket
s.close()
