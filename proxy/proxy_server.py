import http.server
import urllib.parse
import requests
from modifier import *

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
                request = requests.get(httpsoverwrite(url.geturl()), headers=headers)
        except:
                request = requests.get(url.geturl(), headers=headers)
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
                request = requests.post(httpsoverwrite(url.geturl()), headers=headers)
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
                request = requests.put(httpsoverwrite(url.geturl()), headers=headers)
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
                request = requests.delete(httpsoverwrite(url.geturl()), headers=headers)
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
def run_proxy():
    server_address = ('0.0.0.0', 8080)
    httpd = http.server.HTTPServer(server_address, ProxyRequestHandler)
    print("Proxy-Server Started on port 8080")
    httpd.serve_forever()

run_proxy()
