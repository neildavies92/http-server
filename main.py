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

    try:
        if path in ("/", f"/{FILE}"):
            with open(f"www/{FILE}", "r") as f:
                body = f.read()
            response = f"{version} 200 OK\r\n\r\n{body}"
    except FileNotFoundError:
        response = f"{version} 404 File Not Found\r\n\r\n"

    conn.sendall(response.encode("utf-8"))
    conn.close()


def create_thread(handle_request):
    thread = threading.Thread(target=handle_request)
    thread.start()
    print(thread)
    return thread


server = start_server(HOSTNAME, PORT)

while True:
    handle_request(server)

    def handle_connection():
        handle_request(server)

    create_thread(handle_connection)
