
from http.server import HTTPServer,BaseHTTPRequestHandler
import webbrowser

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain ; charset=utf-8')
        self.end_headers()
        self.wfile.write("HELLO WORLD".encode())


if __name__=='__main__':
    server_add=('',8888)
    httpd=HTTPServer(server_add,Handler)
    httpd.serve_forever()
    print('OPENING PAGE')
    webbrowser.open('http://localhost:8888')
    print("OPENED")