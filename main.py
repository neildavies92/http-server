import socket

hostname = 'localhost'
port = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(1)

conn, addr = s.accept()
print(f"Connection from {addr}\n")

request = conn.recv(1024).decode('utf-8')
print(request)

request_lines = request.splitlines()
if request_lines:
    request_line = request_lines[0]
    method, path, version = request_line.split()

if path == '/':
    path = f'/index.html'

with open('www/index.html', 'r') as file:
    body = file.read()

response = (
    f"{version} 200 OK\r\n\n"
    f"{body}"
)
print(response)

conn.sendall(response.encode('utf-8'))
s.close()