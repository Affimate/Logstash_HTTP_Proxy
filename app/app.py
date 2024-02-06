from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from dotenv import load_dotenv
import os
import socket
import asyncio
import json

async def main(bundle, bytes):
    asyncio.ensure_future(fireLost(bundle, bytes))

async def fireLost(bundle, bytes):
    s = socket.socket()
    s.connect(bundle)
    print(bytes)
    s.send(bytes)
    s.close()

class HandleRequests(BaseHTTPRequestHandler):
    def set_proxy_target(self, addr, port):
        self.bundle_target = (addr, port)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.send_response(405)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'')
        
    def do_POST(self):
        '''Reads post request body'''
        self._set_headers()
        content_len = int(self.headers.get_all('content-length')[0])
        post_body = self.rfile.read(content_len)
        now = datetime.now()
        body = post_body.decode().replace("\n","").replace("\t","")
        data = json.loads(body)
        print(data)
        target = self.get_target(data)
        content = json.dumps(data["content"])
        a = "received post request to {}:<br>{}".format(target, content)
        print("["+now.strftime("%m/%d/%Y, %H:%M:%S")+"]: " + a)
        self.delegate_bytes(target, content.encode())
        self.wfile.write(b'')

    def do_PUT(self):
        self.do_POST()

    def get_target(self, data):
        if "target" in data and data["target"] != "" and data["target"].isnumeric():
            return int(data["target"])
        return 0

    def delegate_bytes(self, target, bytes):
        resolve_port = target if target != 0 else self.bundle_target[1]
        asyncio.run(main((self.bundle_target[0], resolve_port), bytes))

if __name__ == "__main__":
    try:
        load_dotenv()
    except Exception:
        pass
    hostName = os.getenv('HOSTNAME')
    serverPort = int(os.getenv('PORT'))
    hostName_target = os.getenv('HOSTNAME_TARGET')
    serverPort_target = os.getenv('PORT_TARGET')
    if type(hostName_target) == type(None) or type(serverPort_target) == type(None):
        print("Undefined Target")
        exit(-1)
    print("HOSTNAME_TARGET:",hostName_target)
    print("PORT_TARGET:",serverPort_target)
    serverPort_target = int(serverPort_target)
    webServer = HTTPServer((hostName, serverPort), HandleRequests)
    webServer.RequestHandlerClass.set_proxy_target(webServer.RequestHandlerClass, hostName_target, serverPort_target)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")