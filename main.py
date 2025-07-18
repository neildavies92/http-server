from http.server import HTTPServer, BaseHTTPRequestHandler

def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('localhost', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run_server()