from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello from Python server inside Docker!")

def main():
    a = Test('Yay')
    print(a.value)
    print("Starting HTTP server on port 8080")
    server = HTTPServer(('0.0.0.0', 8080), SimpleHandler)
    server.serve_forever()  # This will block and keep container alive

if __name__ == "__main__":
    main()