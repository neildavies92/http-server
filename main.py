import socket

host = "localhost"
port = 8000
file = "index.html"


def start_server(host, port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return server_socket
    except Exception as e:
        return f"Error starting server: {e}"


def handle_connection(server_socket):
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")

    request = conn.recv(1024).decode()

    request_lines = request.splitlines()

    if request_lines:
        request_line = request_lines[0]
        _, path, version = request_line.split()
    if path == "/":
        path = f"/{file}"

    with open(f"www/{file}", "r") as f:
        body = f.read()
        response = f"{version} 200 OK\r\n\r\n{body}"
        print(response)

    conn.sendall(response.encode())
    conn.close()


server_socket = start_server(host, port)

if isinstance(server_socket, socket.socket):
    print(f"Server started on {host}:{port}")

    while True:
        handle_connection(server_socket)
else:
    print(server_socket)
