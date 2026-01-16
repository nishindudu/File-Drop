import qrcode
import http.server
import argparse
import socket

argparse = argparse.ArgumentParser(description="Generate a QR code for a file download link.")
argparse.add_argument("file_url", type=str, help="The URL of the file to be downloaded.")
args = argparse.parse_args()

filename = args.file_url

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1
    )
    qr.add_data(url)
    qr.make(fit=True)
    print("Scan the following QR code to download the file:")
    qr.print_ascii(invert=True)

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


class singleFileHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def do_GET(self):
        self.path = f'/{filename}'
        return super().do_GET()


ip = get_local_ip()

server_address = ('', 8000)
http_serv = singleFileHandler
httpd = http.server.HTTPServer(server_address, http_serv)

def start_http_server():
    print("Starting HTTP server on port 8000...")
    httpd.handle_request()
    httpd.server_close()

generate_qr_code(str(f'http://{ip}:8000/{filename}'))
start_http_server()