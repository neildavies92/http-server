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
    print(f"Request: {request}")

    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    if file in ("/", "/index.html"):
        with open(file, "r") as f:
            response += f.read()

    conn.sendall(response.encode())
    conn.close()


server_socket = start_server(host, port)

if isinstance(server_socket, socket.socket):
    print(f"Server started on {host}:{port}")
    while True:
        handle_connection(server_socket)
else:
    print(server_socket)
