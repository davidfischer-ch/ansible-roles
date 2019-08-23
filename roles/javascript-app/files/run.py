#!/usr/bin/env python3

"""
See:

http://stackoverflow.com/users/1074592/fakerainbrigand
http://stackoverflow.com/questions/15401815/python-simplehttpserver
"""

import http.server, os, signal, sys, socketserver, urllib

PORT = 8000
DIRECTORY = os.getcwd()


def main():
    with socketserver.TCPServer(('', PORT), Handler) as server:

        def cleanup_server(signal, frame):
            print('Stopping server...', signal)
            server.server_close()
            sys.exit(0)

        print('Serving content as http://localhost:{0}'.format(PORT))
        signal.signal(signal.SIGINT, cleanup_server)
        server.serve_forever()


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path.lstrip('/')
        if os.access(os.path.join(DIRECTORY, path), os.R_OK):
            return super().do_GET()

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open('index.html', 'rb') as f:
            self.copyfile(f, self.wfile)


if __name__ == '__main__':
    main()
