import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess

class SimpleHandler(BaseHTTPRequestHandler):
    max_post_size = 5 * 1024  # Default to 5KB

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers.get('Content-Length', 0))

            if content_length > self.max_post_size:
                self.send_response(413)
                self.end_headers()
                self.wfile.write(b'Request body too large')
                return

            post_data = self.rfile.read(content_length)
            payload = post_data.decode('utf-8', errors='replace')
            try:
                # Execute ichiran-cli with the given input
                result = subprocess.run(
                    ['ichiran-cli', '-f', payload],
                    capture_output=True,
                    text=True,
                    check=True
                )
                output = result.stdout
                self.send_response(200)
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error running ichiran-cli: {e}'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

def run_server(port, max_size_kb):
    handler_class = SimpleHandler
    handler_class.max_post_size = max_size_kb * 1024

    server_address = ('', port)
    httpd = HTTPServer(server_address, handler_class)
    print(f"Starting server on port {port} (max payload {max_size_kb}KB)...")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple HTTP Server with ichiran-cli')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    parser.add_argument('--max-size', type=int, default=5, help='Maximum POST payload size in KB')
    args = parser.parse_args()

    run_server(args.port, args.max_size)