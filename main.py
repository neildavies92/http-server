import socket

hostname = 'localhost'
port = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(1)

conn, addr = s.accept()
print(f"Connection from {addr}")

conn.send(b"Hello, world!")
conn.close()
s.close()