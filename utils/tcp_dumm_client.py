from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost",5555))
s.listen(1)
conn = False
while True:
    conn, client = s.accept()
    
    try:
        data = conn.recv(512).decode(errors='ignore')
        print(client, data)
        if data == "Hello":
            conn.send("world!\n".encode())
            while conn:
                data = conn.recv(512).decode(errors='ignore')
                if data == "1": print("BEAT")
        elif data == "Command":
            conn.send((input()+"\r").encode())
    except Exception as e:
        print('Error: ', e)
    finally:
        conn.close()
