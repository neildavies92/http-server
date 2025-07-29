import socket
import threading
import os

host = "localhost"
port = 8000
filename = "index.html"


def start_server(host, port):
    """
    Start a TCP server on the specified host and port.

    Args:
        host (str): The host address to bind to (e.g., 'localhost')
        port (int): The port number to bind to

    Returns:
        socket.socket: A configured server socket ready to accept connections

    Raises:
        RuntimeError: If there's an error starting the server (e.g., port already in use)
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        return server_socket
    except Exception as e:
        raise RuntimeError(f"Error starting server: {e}")


def is_safe_path(requested_path, base_dir="www"):
    """
    Check if the requested path is safe and within the base directory.

    This function prevents directory traversal attacks by ensuring that the
    requested file path cannot access files outside the specified base directory.

    Args:
        requested_path (str): The file path requested by the client
        base_dir (str): The base directory that files must be contained within

    Returns:
        bool: True if the path is safe and within the base directory, False otherwise
    """
    requested_path = os.path.normpath(requested_path)
    base_abs = os.path.abspath(base_dir)
    requested_abs = os.path.abspath(os.path.join(base_dir, requested_path))
    return requested_abs.startswith(base_abs)


def handle_connection(conn):
    """
    Handle an individual client connection.

    This function processes HTTP requests from clients, serves files from the
    www directory, and sends appropriate HTTP responses. It includes security
    measures to prevent directory traversal attacks.

    Args:
        conn (socket.socket): The client connection socket
    """
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
        if not is_safe_path(filepath):
            raise FileNotFoundError("Path traversal not allowed")

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
