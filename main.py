import socket

hostname = "localhost"
port = 8000
file = "index.html"


def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((hostname, port))
        s.listen(1)
        print(f"Listening on http://{hostname}:{port}...")
        return s
    except Exception as e:
        print(f"Error creating socket: {e}")
        return None


s = create_socket()
if s is None:
    exit(1)

while True:
    conn, addr = s.accept()
    print(f"Connection from {addr}\n")

    request = conn.recv(1024).decode("utf-8")
    print(request)

    request_lines = request.splitlines()
    if request_lines:
        request_line = request_lines[0]
        method, path, version = request_line.split()

    if path in ("/", f"/{file}"):
        with open("www/index.html", "r") as f:
            body = f.read()
        response = f"{version} 200 OK\r\n\r\n" f"{body}"
    else:
        response = f"{version} 404 File Not Found\r\n\r\n"
    conn.sendall(response.encode("utf-8"))
    conn.close()
