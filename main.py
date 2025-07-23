import socket
import threading

HOSTNAME = "localhost"
PORT = 8000
FILE = "index.html"


def start_server(host, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        print(f"Listening on http://{host}:{port}...")
    except OSError as e:
        return f"Error setting up server: {e}"
    return server


def handle_request(server):
    conn, addr = server.accept()
    data = conn.recv(1024).decode("utf-8")
    print(f"Connection from {addr}\n")

    request_lines = data.splitlines()
    if request_lines:
        request_line = request_lines[0]
        method, path, version = request_line.split()

    if path in ("/", f"/{FILE}"):
        with open(f"www/{FILE}", "r") as f:
            body = f.read()
        response = f"{version} 200 OK\r\n\r\n{body}"
    else:
        response = f"{version} 404 File Not Found\r\n\r\n"

    conn.sendall(response.encode("utf-8"))
    conn.close()


server = create_socket(HOSTNAME, PORT)

while True:
    handle_request(server)
