from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Kirjautumisen käsittely polkuun /login
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Puretaan POST-datat
            post_params = urllib.parse.parse_qs(post_data)

            username = post_params.get('username', [None])[0]
            password = post_params.get('password', [None])[0]

            # Tarkista kirjautumistiedot
            if username == 'admin' and password == 'letmein':
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Login successful!')
            else:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'403 Forbidden: Invalid username or password')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_GET(self):
        # Palautetaan yksinkertainen kirjautumislomake
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
            <html>
                <body>
                    <h2>Login</h2>
                    <form action="/login" method="POST">
                        <input type="text" name="username" placeholder="Username" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <button type="submit">Login</button>
                    </form>
                </body>
            </html>
        """)

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8080)  # Kuuntelee kaikilta IP-osoitteilta portissa 8080
    httpd = server_class(server_address, handler_class)
    print("Server running on port 8080...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
