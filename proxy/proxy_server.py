import http.server
import urllib.parse
import requests
from modifier import *
import socket
import select
import socketserver
import ssl

# This is my https to http conversion proxy.
# It is very basic and should not be used in
# production eviroments. The proxy sets the
# User-agent to IE 6.0 as its the most common
# browser of the era, and other browsers like
# IE 5 work fine or firefox 2 still work fine
# with this setting. If you want any other
# browser, just replace the useragents with
# the ones of the browser you want. Also the
# OS gets reportet as windows 95 as thats what
# I tested this proxy on.


class ProxyRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        headers = {
               'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows 95; SV1)',
        }
        try:
                request = requests.get(urlmodifier(url.geturl()), headers=headers)
        except:
                try:
                        request = requests.get(url.geturl(), headers=headers)
                except:
                        self.send_error(503)
                        return
        type = request.headers["content-type"]
        if type.startswith("text/"):
                request = request.text
                request = codemodifier(request)
                response = b""
                response = response + bytes(request, 'utf-8')
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(response)
        else:
                request = request.content
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(request)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        headers = {
               'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows 95; SV1)',
        }
        try:
                request = requests.post(urlmodifier(url.geturl()), headers=headers)
        except:
                request = requests.post(url.geturl(), headers=headers)
        type = request.headers["content-type"]
        if type.startswith("text/"):
                request = request.text
                request = codemodifier(request)
                response = b""
                response = response + bytes(request, 'utf-8')
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(response)
        else:
                request = request.content
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(request)

    def do_PUT(self):
        url = urllib.parse.urlparse(self.path)
        headers = {
               'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows 95; SV1)',
        }
        try:
                request = requests.put(urlmodifier(url.geturl()), headers=headers)
        except:
                request = requests.put(url.geturl(), headers=headers)
        type = request.headers["content-type"]
        if type.startswith("text/"):
                request = request.text
                request = codemodifier(request)
                response = b""
                response = response + bytes(request, 'utf-8')
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(response)
        else:
                request = request.content
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(request)

    def do_DELETE(self):
        url = urllib.parse.urlparse(self.path)
        headers = {
               'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows 95; SV1)',
        }
        try:
                request = requests.delete(urlmodifier(url.geturl()), headers=headers)
        except:
                request = requests.delete(url.geturl(), headers=headers)
        type = request.headers["content-type"]
        if type.startswith("text/"):
                request = request.text
                request = codemodifier(request)
                response = b""
                response = response + bytes(request, 'utf-8')
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(response)
        else:
                request = request.content
                self.send_response(200)
                self.send_header('Content-type', type)
                self.send_header('Content-Length', str(len(request)))
                self.end_headers()
                self.wfile.write(request)
        
    def do_HEAD(self):
        url = urllib.parse.urlparse(self.path)
        headers = {
               'User-Agent': 'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows 95; SV1)',
        }
        try:
                request = requests.head(urlmodifier(url.geturl()), headers=headers)
        except Exception:
                request = requests.head(url.geturl(), headers=headers)
                type = request.headers.get("content-type", "")
                self.send_response(200)
                if type:
                        self.send_header('Content-type', type)
                        self.end_headers()
        
    def do_PROPFIND(self):
            url = urllib.parse.urlparse(self.path)
            headers = ["User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows 95)"]
            content_length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(content_length) if content_length > 0 else None
            try:
                    request = requests.request("PROPFIND", urlmodifier(url.geturl()), headers=headers, data=data)
            except Exception:
                    request = requests.request("PROPFIND", url.geturl(), headers=headers, data=data)
            type = request.headers.get("content-type", "")
            if type.startswith("text/"):
                    content = codemodifier(request.text)
                    response = content.encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-type', type)
                    self.send_header('Content-Length', str(len(response)))
                    self.end_headers()
                    self.wfile.write(response)
            else:
                    content = request.content
                    self.send_response(200)
                    if type:
                            self.send_header('Content-type', type)
                    self.send_header('Content-Length', str(len(content)))
                    self.end_headers()
                    self.wfile.write(content)

        
    def do_CONNECT(self):
            # This code was also written by ChatGPT, I looked through the code and it appears to be fine.
            # The fact that TLS 1.0 and 1.1 are no longer supported makes this experimental
            # This is also why I didn't bundle a certificate with this project
            MITM_MODE = False  # Switch between MITM (experimental) and normal mode
            host, port = self.path.split(":")
            port = int(port)
            try:
                if MITM_MODE:
                    self.send_response(200, "Connection Established")
                    self.end_headers()

                    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                    context.minimum_version = ssl.TLSVersion.TLSv1
                    context.maximum_version = ssl.TLSVersion.TLSv1
                    context.load_cert_chain(certfile="mitm_cert.pem", keyfile="mitm_key.pem")
                    client_ssl = context.wrap_socket(self.connection, server_side=True)

                    remote_sock = socket.create_connection((host, port))
                    remote_ssl = ssl.create_default_context().wrap_socket(remote_sock, server_hostname=host)

                    sockets = [client_ssl, remote_ssl]
                    while True:
                        rlist, _, _ = select.select(sockets, [], [], 1)
                        for s in rlist:
                            data = s.recv(4096)
                            if not data:
                                return
                            if s is client_ssl:
                                remote_ssl.sendall(data)
                            else:
                                client_ssl.sendall(data)

                else:
                    # Do normal CONNECT stuff
                    with socket.create_connection((host, port)) as remote:
                        self.send_response(200, "Connection Established")
                        self.end_headers()
                        sockets = [self.connection, remote]
                        while True:
                            rlist, _, _ = select.select(sockets, [], [], 1)
                            for s in rlist:
                                data = s.recv(4096)
                                if not data:
                                    return
                                if s is self.connection:
                                    remote.sendall(data)
                                else:
                                    self.connection.sendall(data)

            except Exception as e:
                self.send_error(502, str(e))


def run_proxy():
    server_address = ('0.0.0.0', 8080)
    httpd = socketserver.ThreadingTCPServer(server_address, ProxyRequestHandler)
    print("Proxy-Server Started on port 8080")
    httpd.serve_forever()

run_proxy()
