import socket

hostname = 'localhost'
port = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))
s.listen(1)

conn, addr = s.accept()
print(f"Connection from {addr}\n")

request = conn.recv(1024)
request_text = request.decode('utf-8')
print(request_text)

request_lines = request_text.splitlines()
if request_lines:
    request_line = request_lines[0]
    method, path, version = request_line.split()
    print(f"Method: {method}, Path: {path}, Version: {version}")

response = (
    f"{version} 200 OK\r\n"
    f"Requested path: {path}\r\n"
)
conn.sendall(response.encode('utf-8'))
s.close()