import socket

client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",9999))

message = client.recv(1024).decode()
print(message)
client.send(input(message).encode())
#display the msg to get the user input,it'll be encoded and sent to server
message = client.recv(1024).decode()
print(message)
client.send(input(message).encode())

response= client.recv(1024).decode()
print(response)

client.close()