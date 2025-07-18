import socket

hostname = 'localhost'
port = 80
file = 'index.html'

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

if path in ('/', f'/{file}'):
    with open('www/index.html', 'r') as f:
        body = f.read()
    response = (
        f"{version} 200 OK\r\n\r\n"
        f"{body}"
    )
else:
    response = (
        f"{version} 404 File Not Found\r\n\r\n"
    )

conn.sendall(response.encode('utf-8'))
s.close()