#!/usr/bin/env python3
"""Static file server for local development: python3 serve.py [port]"""
import http.server
import os
import socketserver
import sys

port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
os.chdir(os.path.dirname(os.path.abspath(__file__)))
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", port), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"Serving on http://localhost:{port}")
    httpd.serve_forever()
