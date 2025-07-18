import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

hostname = 'localhost'
port = 8080

def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (hostname, port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

#TODO: Create a socket, and bind it to the address of your server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((hostname, port))

#TODO: Listen for incoming connections
#TODO: Accept incoming requests
#TODO: Recieve incoming data
#TODO: Close the connection
# run_server()