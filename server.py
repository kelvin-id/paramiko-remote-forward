from http.server import BaseHTTPRequestHandler, HTTPServer

class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Write content as utf-8 data
        self.wfile.write(bytes("<html><head><title>Hello World</title></head><body><h1>Hello World!</h1></body></html>", "utf8"))

if __name__ == "__main__":
    # Define server address and port
    server_address = ('', 9051)  # Listening on all available interfaces

    # Create HTTP server
    httpd = HTTPServer(server_address, HelloWorldHandler)

    # Run server
    print("Serving HTTP on port 9051...")
    httpd.serve_forever()
