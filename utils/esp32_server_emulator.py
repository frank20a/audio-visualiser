from socket import socket

s = socket()
s.bind(('', 25565))

s.listen(5)

c, addr = s.accept()
print(addr[0] + " ACK")
c.send((addr[0] + " ACK").encode())

while True:
    ack = ''
    while ack != "nl":
        ack = c.recv(1024).decode()
        print(ack)
        
    c.send("nl ACK".encode())
    print("Sendind nl ACK")
    for i in range(15):
        col = c.recv(3)
        # print(col)
    print()

c.close() 
