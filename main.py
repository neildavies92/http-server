import socket
import threading

host = "localhost"
port = 8000
filename = "index.html"


def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return server_socket
    except Exception as e:
        raise RuntimeError(f"Error starting server: {e}")


def handle_connection(conn):
    print(f"Connection from {conn.getpeername()}")

    request = conn.recv(1024).decode()

    request_lines = request.splitlines()

    if request_lines:
        request_line = request_lines[0]
        _, path, version = request_line.split()

    if path == "/":
        path = f"/{filename}"

    try:
        filepath = path.lstrip("/")
        if not filepath:
            filepath = filename
        with open(f"www/{filepath}", "r") as f:
            body = f.read()
            response = f"{version} 200 OK\r\n\r\n{body}"
    except FileNotFoundError:
        with open("www/error.html", "r") as f:
            body = f.read()
        response = f"{version} 404 Not Found\r\n\r\n{body}"

    conn.sendall(response.encode())
    conn.close()


server_socket = start_server(host, port)

if isinstance(server_socket, socket.socket):
    print(f"Server started on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()
        print(thread)
else:
    print(server_socket)
